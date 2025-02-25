'''
Created on Mar 28, 2015

uploads the archive contents that meet the specified conditions to GCS

Copyright 2015, Institute for Systems Biology.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: michael
'''
import os
import shutil

import util

def get_bucket_key_prefix(config, metadata):
    '''
    returns the GCS bucket and object key to use in the upload of the files in the archive
    
    parameters:
        config: the configuration map
        metadata: the map with archive metadata
    
    returns:
        bucket_name: the bucket name to store the files
        key: the object key to prefix the file names
    '''
    # note that in an archive, all the files will share the same values for these fields
    open_access = config['access_tags']['open']
    if open_access == metadata['SecurityProtocol']:
        bucket_name = config['buckets']['open']
    else:
        bucket_name = config['buckets']['controlled']
    key = '/%s/%s/%s/%s/' % (metadata['Project'].lower(), metadata['Study'].lower(), metadata['Platform'], metadata['Pipeline'])
    return bucket_name, key

def upload_files(config, archive_path, file2metadata, log):
    '''
    uploads the files in the archive_path folder
    
    parameters:
        config: the configuration map
        archive_path: folder archive was downloaded to and the files extracted to
        file2metadata: map of file to its metadata
        log: logger to log any messages
    '''
    files = os.listdir(archive_path)
    if 0 < len(files):
        bucket_name, key_prefix = get_bucket_key_prefix(config, file2metadata[files[0]])
        for file_name in files:
            metadata = file2metadata[file_name]
            key_name = key_prefix + metadata['DataLevel'].replace(' ', '_') + '/'+ file_name
            if config['upload_files']:
                util.upload_file(config, archive_path + file_name, bucket_name, key_name, log)
    else:
        log.warning('\tno files for %s' % (archive_path))
 
def upload_file(filename, metadata, nonupload_files, exclude_samples, level, log):
    '''
    determines if the file should be uploaded.  the file must be the same level as the archive and not a 
    control file; must not have an annotation that excludes it; must not have been preserved with the 
    ffpe protocol; must not have been marked to be excluded in the SDRF; and must not have an extension
    in the nonupload_files list
    
    parameters:
        filename: the name of the file
        metadata: the file metadata
        nonupload_files: list of file extensions of files not to upload
        exclude_samples: list of ffpe preserved samples or samples without a project assigned not to upload
        level: the level of the archive
        log: logger to log any messages
    
    returns:
        whether to upload the file or not
    '''
    upload = 'true'
    if level != metadata['DataLevel'] or '20' == metadata['AliquotBarcode'][13:15]:
        upload = 'false'
    elif 'AnnotationCategory' in metadata and metadata['AnnotationCategory']:
        log.info('\t\tskipping file %s: \'%s\'' % (filename, metadata['AnnotationCategory']))
        upload = 'false'
    elif metadata['SampleBarcode'] in exclude_samples:
        log.info('\t\tskipping exclude (ffpe or no project) file %s' % (filename))
        upload = 'false'
    elif 'yes' != metadata['IncludeForAnalysis']:
        log.info('\t\tskipping not included file %s' % (filename))
        upload = 'false'
    else:
        for nonupload_file in nonupload_files:
            if ('*' == nonupload_file[0] and nonupload_file[1:-1] in filename) or filename.endswith(nonupload_file):
                log.info('\t\tskipping \'%s\' file %s' % (nonupload_file, filename))
                upload = 'false'
                break
    # DatafileUploaded will be set in a post upload step
    metadata['DatafileUploaded'] = 'false'
    metadata['DatafileNameKey'] = None
    return True if 'true' == upload else False

def process_files(config, archive_path, sdrf_metadata, seen_files, nonupload_files, exclude_samples, level, log):
    '''
    process the files in the archive downloaded to the archive_path folder for
    whether they should be uploaded or not
    
    parameters:
        config: the configuration map
        archive_path: folder archive was downloaded to and the files extracted to
        sdrf_metadata: metadata map to update
        seen_files: files that have been seen in a previously processed archive
        nonupload_files: list of file extensions of files not to upload
        exclude_samples: list of ffpe preserved samples or samples without a project assigned not to upload
        level: the level of the archive
        log: logger to log any messages
    
    returns:
        file2metadata: map of filenames to upload with the metadata
    '''
    files = os.listdir(archive_path)
    metadatafiles = set([curdict.keys()[0] for curdict in sdrf_metadata.values()])
    archiveonly = set(files) - metadatafiles
    if 0 < len(archiveonly):
        log.warning('files only in the archive, not sdrf: %s' % (','.join(archiveonly)))
    
    file2metadata = {}
    filenames = set()
    processed_filenames = set()
    for filename2metadata in sdrf_metadata.itervalues():
        try:
            for filename, metadata in filename2metadata.iteritems():
                if filename in processed_filenames:
                    continue
                processed_filenames.add(filename)
                file2metadata[filename] = metadata
                if upload_file(filename, metadata, nonupload_files, exclude_samples, level, log):
                    filenames.add(filename)
        except:
            log.exception('problem looking up %s in metadata' % filename)
    
    # setup the directory so only files to be uploaded remain in the directory
    for file_name in files:
        if file_name not in filenames or file_name in seen_files:
            if file_name in seen_files:
                log.warning('\t\tfound repeated file %s' % (file_name))
            os.remove(archive_path + file_name)
        else:
            seen_files.add(file_name)
            log.info('\t\tuploading %s' % (file_name))
    return file2metadata

def upload_archive(config, sdrf_metadata, archive2metadata, exclude_samples, archive_fields, upload_archives, seen_files, nonupload_files, access, log):
    '''
    uploads the files in the archive that meet the conditions
    
    parameters:
        config: the configuration map
        sdrf_metadata: metadata map to update
        archive2metadata: archive metadata
        exclude_samples: list of ffpe preserved samples or samples without a project assigned not to upload
        archive_fields: archive name, creation date, and URL
        upload_archives: map of level to center to platform of archives to upload
        seen_files: files that have been seen in a previously processed archive
        nonupload_files: list of file extensions of files not to upload
        access: either open or controlled
        log: logger to log any messages
    '''
    archive_path = None
    if config['download_archives'] and util.is_upload_archive(archive_fields[0], upload_archives, archive2metadata):
        log.info('\tuploading %s-access archive %s.' % (access, archive_fields[0]))
        try:
            level = archive_fields[0].split('.')[-4].replace('_', ' ')
            user_info = config['user_info']
            archive_path = util.setup_archive(config, archive_fields, log, user_info['user'], user_info['password'])
            file2metadata = process_files(config, archive_path, sdrf_metadata, seen_files, nonupload_files, exclude_samples, level, log)
            if 0 < len(file2metadata):
                upload_files(config, archive_path, file2metadata, log)
            else:
                log.warning('did not find files to load for %s' % (archive_fields[0]))
        finally:
            if archive_path:
                shutil.rmtree(archive_path)
        log.info('\tfinished uploading %s-access archive %s' % (access, archive_fields[0]))
    else:
        log.info('\tskipping %s-access archive %s' % (access, archive_fields[0]))

def upload_archives(config, log, archives, sdrf_metadata, archive2metadata, exclude_samples):
    '''
    process the metadata and upload the files from the archives
    
    parameters:
        config: the configuration map
        log: logger to log any messages
        archives: the list of archives
        sdrf_metadata: metadata map to update
        archive2metadata: archive metadata
        exclude_samples: list of ffpe preserved samples or samples without a project assigned not to upload
    
    returns:
        sdrf_metadata: the updated metadata map
    '''
    log.info('start upload archives')
    upload_archives = config['upload_archives']
    nonupload_files = config['nonupload_files']
    # the maf related files will be loaded separately
    nonupload_files += config['maf_upload_files']
    archives.sort(key=lambda archive_fields: archive2metadata[archive_fields[0]]['DataArchiveVersion'], reverse=True)
    # track the uploaded file names to avoid uploading duplicates
    seen_files = set()
    for archive_fields in archives:
        if 'tcga4yeo' in archive_fields[2] and config['upload_controlled']:
            upload_archive(config, sdrf_metadata, archive2metadata, exclude_samples, archive_fields, upload_archives, seen_files, nonupload_files, 'controlled', log)
        if 'tcga4yeo' not in archive_fields[2] and config['upload_open']:
            upload_archive(config, sdrf_metadata, archive2metadata, exclude_samples, archive_fields, upload_archives, seen_files, nonupload_files, 'open', log)

    log.info('finished upload archives')
