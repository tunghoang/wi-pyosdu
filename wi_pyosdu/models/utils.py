__SCHEMA_AUTHORITY = 'osdu'
__DATASET_NAME = 'wks'
OSDU_KINDS = {
  'Organisation': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:master-data--Organisation:1.2.0',
  'Basin': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:master-data--Basin:1.2.0',
  'Well': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:master-data--Well:1.2.0',
  'Wellbore': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:master-data--Wellbore:1.3.0',
  'FileGeneric': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:dataset--File.Generic:1.0.0'
}
OSDU_ID_PREFIXES = {
  'Organisation': f'{__SCHEMA_AUTHORITY}:master-data--Organisation',
  'Basin': f'{__SCHEMA_AUTHORITY}:master-data--Basin',
  'Well': f'{__SCHEMA_AUTHORITY}:master-data--Well',
  'Wellbore': f'{__SCHEMA_AUTHORITY}:master-data--Wellbore',
  'FileGeneric': f'{__SCHEMA_AUTHORITY}:dataset--File.Generic'
}
