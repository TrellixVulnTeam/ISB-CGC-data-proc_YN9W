"""

Copyright 2019, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
from google.cloud import bigquery
from google.cloud import storage
from google.cloud import exceptions
import shutil
import os
import yaml
import zipfile
import requests
import urllib.parse as up
import subprocess
import csv
import time
import io
import zipfile
import gzip
from json import loads as json_loads

"""
Build a manifest filter using the list of filter items you can get from a GDC search
"""

def build_manifest_filter(filter_dict_list):
    # Note the need to double up the "{{" to make the format command happy:
    filter_template = '''
    {{
        "op": "in",
        "content": {{
            "field": "{0}",
            "value": [
                "{1}"
            ]
        }}
    }}
    '''

    prefix = '''
    {
      "op": "and",
      "content": [

    '''
    suffix = '''
      ]
    }
    '''

    filter_list = []
    for kv_pair in filter_dict_list:
        for k, v in kv_pair.items():
            if len(filter_list) > 0:
                filter_list.append(',\n')
            filter_list.append(filter_template.format(k, v.rstrip('\n')))

    whole_filter = [prefix] + filter_list + [suffix]
    return ''.join(whole_filter)

"""
Get the manifest for the provided filter set from the GDC
"""

def get_the_manifest(filter_string, api_url, manifest_file, max_files=None):

    #
    # 1) When putting the size and "return_type" : "manifest" args inside a POST document, the result comes
    # back as JSON, not the manifest format.
    # 2) Putting the return type as parameter in the URL while doing a post with the filter just returns
    # every file they own (i.e. the filter in the POST doc is ignored, probably to be expected?).
    # 3) Thus, put the filter in a GET request.
    #

    num_files = max_files if max_files is not None else 100000
    request_url = '{}?filters={}&size={}&return_type=manifest'.format(api_url,
                                                                      up.quote(filter_string),
                                                                      num_files)

    resp = requests.request("GET", request_url)

    if resp.status_code == 200:
        mfile = manifest_file
        with open(mfile, mode='wb') as localfile:
            localfile.write(resp.content)
        print("Wrote out manifest file: {}".format(mfile))
        return True
    else:
        print()
        print("Request URL: {} ".format(request_url))
        print("Problem downloading manifest file. HTTP Status Code: {}".format(resp.status_code))
        print("HTTP content: {}".format(resp.content))
        return False

"""
Clean out the target directory tree:
"""

def create_clean_target(local_files_dir):

    if os.path.exists(local_files_dir):
        print("deleting {}".format(local_files_dir))
        try:
            shutil.rmtree(local_files_dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

        print("done {}".format(local_files_dir))

    if not os.path.exists(local_files_dir):
        os.makedirs(local_files_dir)

"""
Run the "Download Client", which now justs hauls stuff out of the cloud buckets
"""

def pull_from_buckets(manifest_file, indexd_max, indexd_url, local_files_dir):

    # Parse the manifest file for uids, pull out other data too as a sanity check:

    manifest_vals = {}
    with open(manifest_file, 'r') as readfile:
        first = True
        for line in readfile:
            if first:
                first = False
                continue
            split_line = line.rstrip('\n').split("\t")
            manifest_vals[split_line[0]] = {
                'filename': split_line[1],
                'md5': split_line[2],
                'size': int(split_line[3])
            }

    # Use IndexD to map to Google bucket URIs. Batch up IndexD calls to reduce API load:

    max_per_call = indexd_max
    indexd_results = {}
    num_full_calls = len(manifest_vals) // max_per_call  # Python 3: // is classic integer floor!
    num_final_call = len(manifest_vals) % max_per_call
    uuid_list = []
    call_count = 0
    for uuid in manifest_vals:
        uuid_list.append(uuid)
        list_len = len(uuid_list)
        is_last = (call_count == num_full_calls)
        if list_len == max_per_call or (is_last and list_len == num_final_call):
            print(uuid_list)
            request_url = '{}{}'.format(indexd_url, ','.join(uuid_list))
            resp = requests.request("GET", request_url)
            file_dict = json_loads(resp.text)
            for i in range(0, list_len):
                call_id = uuid_list[i]
                curr_record = file_dict['records'][i]
                curr_id = curr_record['did']
                manifest_record = manifest_vals[curr_id]
                indexd_results[curr_id] = curr_record
                print(curr_id, call_id, manifest_record['md5'])
                # print( curr_record['did'],  curr_id, curr_record['hashes']['md5'], manifest_record['md5'], curr_record['size'], manifest_record['size'], )
                if curr_record['did'] != curr_id or \
                                curr_record['hashes']['md5'] != manifest_record['md5'] or \
                                curr_record['size'] != manifest_record['size']:
                    raise Exception(
                        "Expected data mismatch! {} vs. {}".format(str(curr_record), str(manifest_record)))
            uuid_list.clear()

    # Use cloud storage client to move the data onto the VM:

    storage_client = storage.Client()
    for uid, record in indexd_results.items():
        url_list = record['urls']
        gs_urls = [g for g in url_list if g.startswith('gs://')]
        if len(gs_urls) != 1:
            raise Exception("More than one gs:// URI! {}".format(str(gs_urls)))
        path_pieces = up.urlparse(gs_urls[0])
        dir_name = os.path.dirname(path_pieces.path)
        make_dir = "{}{}".format(local_files_dir, dir_name)
        os.makedirs(make_dir, exist_ok=True)
        bucket = storage_client.bucket(path_pieces.netloc)
        blob = bucket.blob(path_pieces.path[1:])  # drop leading / from blob name
        full_file = "{}{}".format(local_files_dir, path_pieces.path)
        blob.download_to_filename(full_file)

"""
Build the File List
Using the tree of downloaded files, we build a file list. Note that we see the downloads
(using the GDC download tool) bringing along logs and annotation.txt files, which we
specifically omit.
"""
def build_file_list(local_files_dir):

    print("building file list from {}".format(local_files_dir))
    all_files = []
    for path, dirs, files in os.walk(local_files_dir):
        if not path.endswith('logs'):
            for f in files:
                if f != 'annotations.txt':
                    if f.endswith('parcel'):
                        raise Exception
                    all_files.append('{}/{}'.format(path, f))

    print("done building file list from {}".format(local_files_dir))
    return all_files
