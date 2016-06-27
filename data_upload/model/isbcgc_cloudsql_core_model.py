'''
a wrapper to google cloud sql.

the MySQLdb module is thread safe but the connections to the database are not.  so the
recommendation is that each thread have an independent connection.  currently, each
database access will use its own connection and at the end of the method, close it.
if this becomes expensive, timewise, a mapping of thread to connection can be utilized.

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
'''
from collections import OrderedDict

import isbcgc_cloudsql_model

class ISBCGC_database_helper(isbcgc_cloudsql_model.ISBCGC_database_helper):
    """
    this class manages the cloud sql metadata upload
    """
    metadata_clinical = {
        'table_name': 'metadata_clinical',
        'primary_key_name': 'metadata_clinical_id',
        'columns': [
            ['age_at_initial_pathologic_diagnosis', 'INTEGER', 'NULL'],
            ['age_began_smoking_in_years', 'INTEGER', 'NULL'],
            ['anatomic_neoplasm_subdivision', 'VARCHAR(63)', 'NULL'],
            ['batch_number', 'INTEGER', 'NULL'],
            ['bcr', 'VARCHAR(63)', 'NULL'],
            ['BMI', 'FLOAT(3,1)', 'NULL'],
            ['clinical_M', 'VARCHAR(12)', 'NULL'],
            ['clinical_N', 'VARCHAR(12)', 'NULL'],
            ['clinical_stage', 'VARCHAR(12)', 'NULL'],
            ['clinical_T', 'VARCHAR(12)', 'NULL'],
            ['colorectal_cancer', 'VARCHAR(10)', 'NULL'],
            ['country', 'VARCHAR(63)', 'NULL'],
            ['days_to_birth', 'INTEGER', 'NULL'],
            ['days_to_death', 'INTEGER', 'NULL'],
            ['days_to_initial_pathologic_diagnosis', 'INTEGER', 'NULL'],
            ['days_to_last_followup', 'INTEGER', 'NULL'],
            ['days_to_last_known_alive', 'INTEGER', 'NULL'],
            ['days_to_submitted_specimen_dx', 'INTEGER', 'NULL'],
            ['ethnicity', 'VARCHAR(30)', 'NULL'],
            ['gender', 'VARCHAR(15)', 'NULL'],
            ['gleason_score_combined', 'INTEGER', 'NULL'],
            ['h_pylori_infection', 'VARCHAR(10)', 'NULL'],
            ['height', 'INTEGER', 'NULL'],
            ['histological_type', 'VARCHAR(120)', 'NULL'],
            ['history_of_colon_polyps', 'VARCHAR(8)', 'NULL'],
            ['history_of_neoadjuvant_treatment', 'VARCHAR(63)', 'NULL'],
            ['hpv_calls', 'VARCHAR(20)', 'NULL'],
            ['hpv_status', 'VARCHAR(20)', 'NULL'],
            ['icd_10', 'VARCHAR(8)', 'NULL'],
            ['icd_o_3_histology', 'VARCHAR(10)', 'NULL'],
            ['icd_o_3_site', 'VARCHAR(8)', 'NULL'],
            ['lymphatic_invasion', 'VARCHAR(8)', 'NULL'],
            ['lymphnodes_examined', 'VARCHAR(8)', 'NULL'],
            ['lymphovascular_invasion_present', 'VARCHAR(8)', 'NULL'],
            ['menopause_status', 'VARCHAR(120)', 'NULL'],
            ['mononucleotide_and_dinucleotide_marker_panel_analysis_status', 'VARCHAR(20)', 'NULL'],
            ['neoplasm_histologic_grade', 'VARCHAR(15)', 'NULL'],
            ['new_tumor_event_after_initial_treatment', 'VARCHAR(8)', 'NULL'],
            ['number_of_lymphnodes_examined', 'INTEGER', 'NULL'],
            ['number_of_lymphnodes_positive_by_he', 'INTEGER', 'NULL'],
            ['number_pack_years_smoked', 'INTEGER', 'NULL'],
            ['other_dx', 'VARCHAR(70)', 'NULL'],
            ['other_malignancy_anatomic_site', 'VARCHAR(65)', 'NULL'],
            ['other_malignancy_histological_type', 'VARCHAR(150)', 'NULL'],
            ['other_malignancy_malignancy_type', 'VARCHAR(90)', 'NULL'],
            ['ParticipantBarcode', 'VARCHAR(45)', 'NOT NULL'],
            ['ParticipantUUID', 'VARCHAR(36)', 'NOT NULL'],
            ['pathologic_M', 'VARCHAR(12)', 'NULL'],
            ['pathologic_N', 'VARCHAR(12)', 'NULL'],
            ['pathologic_stage', 'VARCHAR(15)', 'NULL'],
            ['pathologic_T', 'VARCHAR(12)', 'NULL'],
            ['person_neoplasm_cancer_status', 'VARCHAR(15)', 'NULL'],
            ['pregnancies', 'VARCHAR(10)', 'NULL'],
            ['primary_neoplasm_melanoma_dx', 'VARCHAR(10)', 'NULL'],
            ['primary_therapy_outcome_success', 'VARCHAR(70)', 'NULL'],
            ['Project', 'VARCHAR(40)', 'NOT NULL'],
            ['psa_value', 'FLOAT', 'NULL'],
            ['race', 'VARCHAR(50)', 'NULL'],
            ['residual_tumor', 'VARCHAR(5)', 'NULL'],
            ['stopped_smoking_year', 'INTEGER', 'NULL'],
            ['Study', 'VARCHAR(40)', 'NOT NULL'],
            ['tobacco_smoking_history', 'VARCHAR(50)', 'NULL'],
            ['TSSCode', 'VARCHAR(2)', 'NULL'],
            ['tumor_tissue_site', 'VARCHAR(100)', 'NULL'],
            ['tumor_type', 'VARCHAR(30)', 'NULL'],
            ['venous_invasion', 'VARCHAR(8)', 'NULL'],
            ['vital_status', 'VARCHAR(8)', 'NULL'],
            ['weight', 'INTEGER', 'NULL'],
            ['year_of_initial_pathologic_diagnosis', 'INTEGER', 'NULL'],
            ['year_of_tobacco_smoking_onset', 'INTEGER', 'NULL']
        ],
#         'natural_key_cols': [
#             'ParticipantBarcode'
#         ],
        'indices_defs': [
            ['age_at_initial_pathologic_diagnosis'],
            ['age_began_smoking_in_years'],
            ['batch_number'],
            ['bcr'],
            ['BMI'],
            ['clinical_M'],
            ['clinical_N'],
            ['clinical_stage'],
            ['clinical_T'],
            ['colorectal_cancer'],
            ['country'],
            ['days_to_birth'],
            ['days_to_death'],
            ['days_to_last_followup'],
            ['days_to_last_known_alive'],
            ['ethnicity'],
            ['gender'],
            ['gleason_score_combined'],
            ['h_pylori_infection'],
            ['height'],
            ['histological_type'],
            ['history_of_colon_polyps'],
            ['history_of_neoadjuvant_treatment'],
            ['hpv_calls'],
            ['hpv_status'],
            ['icd_10'],
            ['icd_o_3_histology'],
            ['icd_o_3_site'],
            ['lymphatic_invasion'],
            ['lymphovascular_invasion_present'],
            ['menopause_status'],
            ['mononucleotide_and_dinucleotide_marker_panel_analysis_status'],
            ['neoplasm_histologic_grade'],
            ['new_tumor_event_after_initial_treatment'],
            ['number_of_lymphnodes_positive_by_he'],
            ['number_pack_years_smoked'],
            ['ParticipantBarcode'],
            ['pathologic_M'],
            ['pathologic_N'],
            ['pathologic_stage'],
            ['pathologic_T'],
            ['primary_therapy_outcome_success'],
            ['Project'],
            ['psa_value'],
            ['race'],
            ['stopped_smoking_year'],
            ['Study'],
            ['tobacco_smoking_history'],
            ['tumor_tissue_site'],
            ['tumor_type'],
            ['venous_invasion'],
            ['vital_status'],
            ['weight'],
            ['year_of_initial_pathologic_diagnosis'],
            ['year_of_tobacco_smoking_onset']
        ]
    }
    
    metadata_biospecimen = {
        'table_name': 'metadata_biospecimen',
        'primary_key_name': 'metadata_biospecimen_id',
        'columns': [
            ['avg_percent_lymphocyte_infiltration', 'FLOAT', 'NULL'],
            ['avg_percent_monocyte_infiltration', 'FLOAT', 'NULL'],
            ['avg_percent_necrosis', 'FLOAT', 'NULL'],
            ['avg_percent_neutrophil_infiltration', 'FLOAT', 'NULL'],
            ['avg_percent_normal_cells', 'FLOAT', 'NULL'],
            ['avg_percent_stromal_cells', 'FLOAT', 'NULL'],
            ['avg_percent_tumor_cells', 'FLOAT', 'NULL'],
            ['avg_percent_tumor_nuclei', 'FLOAT', 'NULL'],
            ['batch_number', 'INTEGER', 'NULL'],
            ['bcr', 'VARCHAR(63)', 'NULL'],
            ['days_to_collection', 'INTEGER', 'NULL'],
            ['days_to_sample_procurement', 'INTEGER', 'NULL'],
            ['is_ffpe', 'VARCHAR(5)', 'NULL'],
            ['max_percent_lymphocyte_infiltration', 'FLOAT', 'NULL'],
            ['max_percent_monocyte_infiltration', 'FLOAT', 'NULL'],
            ['max_percent_necrosis', 'FLOAT', 'NULL'],
            ['max_percent_neutrophil_infiltration', 'FLOAT', 'NULL'],
            ['max_percent_normal_cells', 'FLOAT', 'NULL'],
            ['max_percent_stromal_cells', 'FLOAT', 'NULL'],
            ['max_percent_tumor_cells', 'FLOAT', 'NULL'],
            ['max_percent_tumor_nuclei', 'FLOAT', 'NULL'],
            ['min_percent_lymphocyte_infiltration', 'FLOAT', 'NULL'],
            ['min_percent_monocyte_infiltration', 'FLOAT', 'NULL'],
            ['min_percent_necrosis', 'FLOAT', 'NULL'],
            ['min_percent_neutrophil_infiltration', 'FLOAT', 'NULL'],
            ['min_percent_normal_cells', 'FLOAT', 'NULL'],
            ['min_percent_stromal_cells', 'FLOAT', 'NULL'],
            ['min_percent_tumor_cells', 'FLOAT', 'NULL'],
            ['min_percent_tumor_nuclei', 'FLOAT', 'NULL'],
            ['num_portions', 'INTEGER', 'NULL'],
            ['num_slides', 'INTEGER', 'NULL'],
            ['ParticipantBarcode', 'VARCHAR(45)', 'NOT NULL'],
            ['Project', 'VARCHAR(40)', 'NOT NULL'],
            ['SampleBarcode', 'VARCHAR(45)', 'NOT NULL'],
            ['SampleType', 'VARCHAR(55)', 'NULL'],
            ['SampleTypeCode', 'VARCHAR(2)', 'NULL'],
            ['SampleTypeLetterCode', 'VARCHAR(5)', 'NULL'],
            ['SampleUUID', 'VARCHAR(36)', 'NULL'],
            ['Study', 'VARCHAR(40)', 'NULL'],
            ['tissue_anatomic_site', 'VARCHAR(55)', 'NULL'],
            ['tissue_anatomic_site_description', 'VARCHAR(45)', 'NULL']
        ],
#         'natural_key_cols': [
#             'SampleBarcode'
#         ],
        'indices_defs': [
            ['batch_number'],
            ['bcr'],
            ['ParticipantBarcode'],
            ['Project'],
            ['SampleBarcode'],
            ['SampleType'],
            ['SampleTypeCode'],
            ['SampleTypeLetterCode'],
            ['Study'],
            ['tissue_anatomic_site'],
            ['tissue_anatomic_site_description']
        ],
#         'foreign_key': [
#             'ParticipantBarcode',
#             'metadata_clinical',
#             'ParticipantBarcode'
#         ]
    }
    
    metadata_data = {
        'table_name': 'metadata_data',
        'primary_key_name': 'metadata_data_id',
        'columns': [
            ['ParticipantBarcode', 'VARCHAR(35)', 'NOT NULL'],
            ['SampleBarcode', 'VARCHAR(45)', 'NOT NULL'],
            ['AliquotBarcode', 'VARCHAR(45)', 'NOT NULL'],
            ['AliquotUUID', 'VARCHAR(36)', 'NULL'],
            ['DataArchiveName', 'VARCHAR(100)', 'NULL'],
            ['DataArchiveURL', 'VARCHAR(300)', 'NULL'],
            ['DataArchiveVersion', 'VARCHAR(20)', 'NULL'],
            ['DataCenterCode', 'VARCHAR(2)', 'NULL'],
            ['DataCenterName', 'VARCHAR(40)', 'NULL'],
            ['DataCenterType', 'VARCHAR(4)', 'NULL'],
            ['DatafileMD5', 'VARCHAR(32)', 'NULL'],
            ['DatafileName', 'VARCHAR(250)', 'NOT NULL'],
            ['DatafileNameKey', 'VARCHAR(300)', 'NOT NULL'],
            ['DatafileUploaded', 'VARCHAR(5)', 'NOT NULL'],
            ['DataLevel', 'VARCHAR(7)', 'NOT NULL'],
            ['Datatype', 'VARCHAR(50)', 'NULL'],
            ['GenomeReference', 'VARCHAR(32)', 'NULL'],
            ['IncludeForAnalysis', 'VARCHAR(3)', 'NULL'],
            ['MAGETabArchiveName', 'VARCHAR(250)', 'NULL'],
            ['MAGETabArchiveURL', 'VARCHAR(300)', 'NULL'],
            ['Pipeline', 'VARCHAR(45)', 'NOT NULL'],
            ['Platform', 'VARCHAR(40)', 'NOT NULL'],
            ['Project', 'VARCHAR(40)', 'NOT NULL'],
            ['Repository', 'VARCHAR(15)', 'NULL'],
            ['SampleType', 'VARCHAR(55)', 'NULL'],
            ['SampleTypeCode', 'VARCHAR(2)', 'NULL'],
            ['SDRFFileName', 'VARCHAR(75)', 'NULL'],
            ['SDRFFileNameKey', 'VARCHAR(200)', 'NULL'],
            ['SecurityProtocol', 'VARCHAR(30)', 'NOT NULL'],
            ['Species', 'VARCHAR(25)', 'NOT NULL'],
            ['Study', 'VARCHAR(40)', 'NOT NULL'],
            ['wasDerivedFrom', 'VARCHAR(1000)', 'NULL'],
            ['library_strategy', 'VARCHAR(25)', 'NULL'],
            ['state', 'VARCHAR(25)', 'NULL'],
            ['reason_for_state', 'VARCHAR(250)', 'NULL'],
            ['analysis_id', 'VARCHAR(36)', 'NULL'],
            ['analyte_code', 'VARCHAR(2)', 'NULL'],
            ['last_modified', 'DATE', 'NULL'],
            ['platform_full_name', 'VARCHAR(30)', 'NULL'],
            ['GG_dataset_id', 'VARCHAR(30)', 'NULL'],
            ['GG_readgroupset_id', 'VARCHAR(40)', 'NULL']
        ],
#         'natural_key_cols': [
#             'AliquotBarcode',
#             'DatafileName'
#         ],
        'indices_defs': [
            ['ParticipantBarcode'],
            ['SampleBarcode'],
            ['AliquotBarcode'],
            ['AliquotUUID'],
            ['DataArchiveName'],
            ['DataArchiveURL'],
            ['DataCenterCode'],
            ['DataCenterName'],
            ['DataCenterType'],
            ['DatafileName'],
            ['DatafileNameKey'],
            ['DatafileUploaded'],
            ['DataLevel'],
            ['Datatype'],
            ['IncludeForAnalysis'],
            ['Pipeline'],
            ['Platform'],
            ['Project'],
            ['Repository'],
            ['SampleType'],
            ['SampleTypeCode'],
            ['SecurityProtocol'],
            ['Species'],
            ['Study'],
            ['state'],
            ['GG_dataset_id']
        ],
#         'foreign_key': [
#             'SampleBarcode',
#             'metadata_biospecimen',
#             'SampleBarcode'
#         ]
    }

    metadata_samples = {
        'table_name': 'metadata_samples',
        'primary_key_name': 'metadata_samples_id',  # todo: define this?

        'columns': [
            ['age_at_initial_pathologic_diagnosis', 'INTEGER', 'NULL'],
            ['anatomic_neoplasm_subdivision', 'VARCHAR(63)', 'NULL'],
            ['age_began_smoking_in_years', 'INTEGER', 'NULL'],
            ['avg_percent_lymphocyte_infiltration', 'FLOAT', 'NULL'],
            ['avg_percent_monocyte_infiltration', 'FLOAT', 'NULL'],
            ['avg_percent_necrosis', 'FLOAT', 'NULL'],
            ['avg_percent_neutrophil_infiltration', 'FLOAT', 'NULL'],
            ['avg_percent_normal_cells', 'FLOAT', 'NULL'],
            ['avg_percent_stromal_cells', 'FLOAT', 'NULL'],
            ['avg_percent_tumor_cells', 'FLOAT', 'NULL'],
            ['avg_percent_tumor_nuclei', 'FLOAT', 'NULL'],
            ['batch_number', 'INTEGER', 'NULL'],
            ['bcr', 'VARCHAR(63)', 'NULL'],
            ['BMI', 'FLOAT(3,1)', 'NULL'],
            ['clinical_M', 'VARCHAR(12)', 'NULL'],
            ['clinical_N', 'VARCHAR(12)', 'NULL'],
            ['clinical_stage', 'VARCHAR(12)', 'NULL'],
            ['clinical_T', 'VARCHAR(12)', 'NULL'],
            ['colorectal_cancer', 'VARCHAR(10)', 'NULL'],
            ['country', 'VARCHAR(63)', 'NULL'],
            ['days_to_birth', 'INTEGER', 'NULL'],
            ['days_to_collection', 'INTEGER', 'NULL'],
            ['days_to_death', 'INTEGER', 'NULL'],
            ['days_to_initial_pathologic_diagnosis', 'INTEGER', 'NULL'],
            ['days_to_last_followup', 'INTEGER', 'NULL'],
            ['days_to_last_known_alive', 'INTEGER', 'NULL'],
            ['days_to_submitted_specimen_dx', 'INTEGER', 'NULL'],
            ['ethnicity', 'VARCHAR(30)', 'NULL'],
            ['gender', 'VARCHAR(15)', 'NULL'],
            ['gleason_score_combined', 'INTEGER', 'NULL'],
            ['h_pylori_infection', 'VARCHAR(10)', 'NULL'],
            ['height', 'INTEGER', 'NULL'],
            ['histological_type', 'VARCHAR(120)', 'NULL'],
            ['history_of_colon_polyps', 'VARCHAR(8)', 'NULL'],
            ['history_of_neoadjuvant_treatment', 'VARCHAR(63)', 'NULL'],
            ['hpv_calls', 'VARCHAR(20)', 'NULL'],
            ['hpv_status', 'VARCHAR(20)', 'NULL'],
            ['icd_10', 'VARCHAR(8)', 'NULL'],
            ['icd_o_3_histology', 'VARCHAR(10)', 'NULL'],
            ['icd_o_3_site', 'VARCHAR(8)', 'NULL'],
            ['lymphatic_invasion', 'VARCHAR(8)', 'NULL'],
            ['lymphnodes_examined', 'VARCHAR(8)', 'NULL'],
            ['lymphovascular_invasion_present', 'VARCHAR(8)', 'NULL'],
            ['max_percent_lymphocyte_infiltration', 'FLOAT', 'NULL'],
            ['max_percent_monocyte_infiltration', 'FLOAT', 'NULL'],
            ['max_percent_necrosis', 'FLOAT', 'NULL'],
            ['max_percent_neutrophil_infiltration', 'FLOAT', 'NULL'],
            ['max_percent_normal_cells', 'FLOAT', 'NULL'],
            ['max_percent_stromal_cells', 'FLOAT', 'NULL'],
            ['max_percent_tumor_cells', 'FLOAT', 'NULL'],
            ['max_percent_tumor_nuclei', 'FLOAT', 'NULL'],
            ['menopause_status', 'VARCHAR(120)', 'NULL'],
            ['min_percent_lymphocyte_infiltration', 'FLOAT', 'NULL'],
            ['min_percent_monocyte_infiltration', 'FLOAT', 'NULL'],
            ['min_percent_necrosis', 'FLOAT', 'NULL'],
            ['min_percent_neutrophil_infiltration', 'FLOAT', 'NULL'],
            ['min_percent_normal_cells', 'FLOAT', 'NULL'],
            ['min_percent_stromal_cells', 'FLOAT', 'NULL'],
            ['min_percent_tumor_cells', 'FLOAT', 'NULL'],
            ['min_percent_tumor_nuclei', 'FLOAT', 'NULL'],
            ['mononucleotide_and_dinucleotide_marker_panel_analysis_status', 'VARCHAR(20)', 'NULL'],
            ['neoplasm_histologic_grade', 'VARCHAR(15)', 'NULL'],
            ['new_tumor_event_after_initial_treatment', 'VARCHAR(8)', 'NULL'],
            ['num_portions', 'INTEGER', 'NULL'],
            ['num_slides', 'INTEGER', 'NULL'],
            ['number_of_lymphnodes_examined', 'INTEGER', 'NULL'],
            ['number_of_lymphnodes_positive_by_he', 'INTEGER', 'NULL'],
            ['number_pack_years_smoked', 'INTEGER', 'NULL'],
            ['other_dx', 'VARCHAR(70)', 'NULL'],
            ['other_malignancy_anatomic_site', 'VARCHAR(65)', 'NULL'],
            ['other_malignancy_histological_type', 'VARCHAR(150)', 'NULL'],
            ['other_malignancy_malignancy_type', 'VARCHAR(90)', 'NULL'],
            ['ParticipantBarcode', 'VARCHAR(45)', 'NOT NULL'],
            ['pathologic_M', 'VARCHAR(12)', 'NULL'],
            ['pathologic_N', 'VARCHAR(12)', 'NULL'],
            ['pathologic_stage', 'VARCHAR(15)', 'NULL'],
            ['pathologic_T', 'VARCHAR(12)', 'NULL'],
            ['person_neoplasm_cancer_status', 'VARCHAR(15)', 'NULL'],
            ['pregnancies', 'VARCHAR(10)', 'NULL'],
            ['primary_neoplasm_melanoma_dx', 'VARCHAR(10)', 'NULL'],
            ['primary_therapy_outcome_success', 'VARCHAR(70)', 'NULL'],
            ['Project', 'VARCHAR(40)', 'NOT NULL'],
            ['psa_value', 'FLOAT', 'NULL'],
            ['race', 'VARCHAR(50)', 'NULL'],
            ['residual_tumor', 'VARCHAR(5)', 'NULL'],
            ['SampleBarcode', 'VARCHAR(45)', 'NOT NULL'],
            ['SampleTypeCode', 'VARCHAR(2)', 'NULL'],
            ['stopped_smoking_year', 'INTEGER', 'NULL'],
            ['Study', 'VARCHAR(40)', 'NOT NULL'],
            ['tissue_anatomic_site', 'VARCHAR(55)', 'NULL'],
            ['tissue_anatomic_site_description', 'VARCHAR(45)', 'NULL'],
            ['tobacco_smoking_history', 'VARCHAR(50)', 'NULL'],
            ['TSSCode', 'VARCHAR(2)', 'NULL'],
            ['tumor_tissue_site', 'VARCHAR(100)', 'NULL'],
            ['tumor_type', 'VARCHAR(30)', 'NULL'],
            ['venous_invasion', 'VARCHAR(8)', 'NULL'],
            ['vital_status', 'VARCHAR(8)', 'NULL'],
            ['weight', 'INTEGER', 'NULL'],
            ['year_of_initial_pathologic_diagnosis', 'INTEGER', 'NULL'],
            ['year_of_tobacco_smoking_onset', 'INTEGER', 'NULL'],
            ['has_Illumina_DNASeq', 'tinyint(4)', 'NULL'],
            ['has_BCGSC_HiSeq_RNASeq', 'tinyint(4)', 'NULL'],
            ['has_UNC_HiSeq_RNASeq', 'tinyint(4)', 'NULL'],
            ['has_BCGSC_GA_RNASeq', 'tinyint(4)', 'NULL'],
            ['has_UNC_GA_RNASeq', 'tinyint(4)', 'NULL'],
            ['has_HiSeq_miRnaSeq', 'tinyint(4)', 'NULL'],
            ['has_GA_miRNASeq', 'tinyint(4)', 'NULL'],
            ['has_RPPA', 'tinyint(4)', 'NULL'],
            ['has_SNP6', 'tinyint(4)', 'NULL'],
            ['has_27k', 'tinyint(4)', 'NULL'],
            ['has_450k', 'tinyint(4)', 'NULL']
        ],
        'natural_key_cols': ['SampleBarcode'],
#         'foreign_key': [
#             'SampleBarcode',
#         ]
        'indices_defs': [
            ['age_at_initial_pathologic_diagnosis'],
            ['age_began_smoking_in_years'],
            ['batch_number'],
            ['bcr'],
            ['BMI'],
            ['clinical_M'],
            ['clinical_N'],
            ['clinical_stage'],
            ['clinical_T'],
            ['colorectal_cancer'],
            ['country'],
            ['days_to_birth'],
            ['days_to_death'],
            ['days_to_last_followup'],
            ['days_to_last_known_alive'],
            ['ethnicity'],
            ['gender'],
            ['gleason_score_combined'],
            ['h_pylori_infection'],
            ['height'],
            ['histological_type'],
            ['history_of_colon_polyps'],
            ['history_of_neoadjuvant_treatment'],
            ['hpv_calls'],
            ['hpv_status'],
            ['icd_10'],
            ['icd_o_3_histology'],
            ['icd_o_3_site'],
            ['lymphatic_invasion'],
            ['lymphovascular_invasion_present'],
            ['menopause_status'],
            ['mononucleotide_and_dinucleotide_marker_panel_analysis_status'],
            ['neoplasm_histologic_grade'],
            ['new_tumor_event_after_initial_treatment'],
            ['number_of_lymphnodes_positive_by_he'],
            ['number_pack_years_smoked'],
            ['ParticipantBarcode'],
            ['pathologic_M'],
            ['pathologic_N'],
            ['pathologic_stage'],
            ['pathologic_T'],
            ['primary_therapy_outcome_success'],
            ['Project'],
            ['psa_value'],
            ['race'],
            ['SampleBarcode'],
            ['SampleTypeCode'],
            ['stopped_smoking_year'],
            ['Study'],
            ['tissue_anatomic_site'],
            ['tissue_anatomic_site_description'],
            ['tobacco_smoking_history'],
            ['tumor_tissue_site'],
            ['tumor_type'],
            ['venous_invasion'],
            ['vital_status'],
            ['weight'],
            ['year_of_initial_pathologic_diagnosis'],
            ['year_of_tobacco_smoking_onset'],
        ]
    }
    
    isbcgc_cloudsql_model.ISBCGC_database_helper.metadata_tables = OrderedDict(
        [
            ('metadata_clinical', metadata_clinical),
            ('metadata_biospecimen', metadata_biospecimen),
            ('metadata_data', metadata_data),
            ('metadata_samples', metadata_samples)
        ]
    )

    self = None

    def __init__(self, config, log):
        isbcgc_cloudsql_model.ISBCGC_database_helper.__init__(self, config, log)

    @classmethod
    def initialize(cls, config, log):
        if cls.self:
            log.warning('class has already been initialized')
        else:
            cls.self = ISBCGC_database_helper(config, log)

