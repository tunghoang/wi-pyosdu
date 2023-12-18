__SCHEMA_AUTHORITY = 'osdu'
__DATASET_NAME = 'wks'
OSDU_KINDS = {
  'Organisation': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:master-data--Organisation:1.2.0',
  'Basin': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:master-data--Basin:1.2.0',
  'Well': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:master-data--Well:1.2.0',
  'Wellbore': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:master-data--Wellbore:1.3.0',
  'FileGeneric': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:dataset--File.Generic:1.0.0',
  'SeismicBinGrid': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:work-product-component--SeismicBinGrid:1.0.0',
  'SeismicTraceData': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:work-product-component--SeismicTraceData:1.0.0',
  'SeismicHorizon': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:work-product-component--SeismicHorizon:1.0.0',
  'SeismicFault': f'{__SCHEMA_AUTHORITY}:{__DATASET_NAME}:work-product-component--SeismicFault:1.0.0'
}
OSDU_ID_PREFIXES = {
  'Organisation': f'{__SCHEMA_AUTHORITY}:master-data--Organisation',
  'Basin': f'{__SCHEMA_AUTHORITY}:master-data--Basin',
  'Well': f'{__SCHEMA_AUTHORITY}:master-data--Well',
  'Wellbore': f'{__SCHEMA_AUTHORITY}:master-data--Wellbore',
  'FileGeneric': f'{__SCHEMA_AUTHORITY}:dataset--File.Generic',
  'SeismicBinGrid': f'{__SCHEMA_AUTHORITY}:work-product-component--SeismicBinGrid',
  'SeismicTraceData': f'{__SCHEMA_AUTHORITY}:work-product-component--SeismicTraceData',
  'SeismicHorizon': f'{__SCHEMA_AUTHORITY}:work-product-component--SeismicHorizon',
  'SeismicFault': f'{__SCHEMA_AUTHORITY}:work-product-component--SeismicFault'
}
