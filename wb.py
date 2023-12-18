from knack.log import get_logger
from pathlib import Path
from wbdutil.wrapper.environment_var_helper import EnvironmentVarHelper
from wbdutil.common.file_loader import LasParser, LocalFileLoader, FileUtilities
from wbdutil.service.record_mapper import LasToRecordMapper
from wbdutil.common.configuration import Configuration
from wbdutil.wrapper.json_writer import JsonToFile

from wbdutil.wrapper.osdu_client import OsduClient
from wbdutil.service.well_service import WellBoreService, WellLogService, DataLoaderConflictError

from wi_pyosdu.client.Token import access_token
from wi_pyosdu.client.Search import *
from wi_pyosdu.client.WBD import *
from wi_pyosdu.client.File import *

import json
import re
import argparse
from os import path

from wi_common import *

parser = argparse.ArgumentParser()
parser.add_argument('--print', action='store_true')
parser.add_argument('--convert', action='store_true')
parser.add_argument('--ingest', action='store_true')
parser.add_argument('--well')
parser.add_argument('--dataset')
parser.add_argument('--path')
parser.add_argument('--get', action="store_true")
parser.add_argument('--list_wells', action="store_true")
parser.add_argument('--list_datasets', action="store_true")
parser.add_argument('--list_curves', action="store_true")
parser.add_argument('--delete', action='store_true')
parser.add_argument('--export', action='store_true')
parser.add_argument('--curves')
parser.add_argument('--out_file')
parser.add_argument('--origin', action='store_true')
args = parser.parse_args()

logger = get_logger(__name__)
token = access_token()

config_path = EnvironmentVarHelper.get_config_path('config.json')

config = Configuration(LocalFileLoader(), config_path)
client = OsduClient(config, token)
wlSvc = WellLogService(client)
wbSvc = WellBoreService(client, wlSvc)


def __get_wellbore_id(well):
    return f"osdu:master-data--Wellbore:{well}" if well else None

def __get_welllog_id(dataset):
    return f"osdu:work-product-component--WellLog:{dataset}" if dataset else None

def print_las_header(input_path):
    las_parser = LasParser(LocalFileLoader())
    for file_path in FileUtilities.get_filenames(Path(input_path), '.las'):
        logger.warning(f"LAS file: {file_path}")
        las_data = las_parser.load_las_file(file_path)
        print(las_data.header)

def convert_las_to_json(input_path, wellbore_id=None, welllog_id=None, config_path = None):
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    las_parser = LasParser(LocalFileLoader())
    config = Configuration(LocalFileLoader(), config_path)

    logger.info(f"LAS path: {input_path}")
    for file_path in FileUtilities.get_filenames(Path(input_path), '.las'):
        logger.error(f"LAS file: {file_path}")
        las_data = las_parser.load_las_file(file_path)
        logger.error("las load done")
        mapper = LasToRecordMapper(las_data, config)
        wellbore_record = mapper.map_to_wellbore_record(wellbore_id)
        welllog_record = mapper.map_to_well_log_record(wellbore_id, welllog_id)

        path = Path(file_path)
        writer = JsonToFile()

        writer.write(wellbore_record.get_raw_data(), path.with_suffix('.wellbore.json'))
        logger.warning(f"Wellbore record file created: {path.with_suffix('.wellbore.json')}")
        writer.write(welllog_record.get_raw_data(), path.with_suffix('.welllog.json'))
        logger.warning(f"Well log record file created: {path.with_suffix('.welllog.json')}")

def convert_las_to_record(input_path, wellbore_id=None, welllog_id=None, config_path = None):
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    las_parser = LasParser(LocalFileLoader())
    config = Configuration(LocalFileLoader(), config_path)
    results = []

    logger.info(f"LAS path: {input_path}")
    for file_path in FileUtilities.get_filenames(Path(input_path), '.las'):
        print(wellbore_id)
        logger.warning(f"LAS file: {file_path}")
        las_data = las_parser.load_las_file(file_path)

        mapper = LasToRecordMapper(las_data, config)
        wellbore_record = mapper.map_to_wellbore_record(wellbore_id)
        welllog_record = mapper.map_to_well_log_record(wellbore_id, welllog_id)
        welllog_data = mapper.extract_log_data()
        results.append({
            'wellbore':wellbore_record,
            'welllog':welllog_record,
            'welllog_data':welllog_data
        })
    return results

def __upload_file(input_path):
    filename = path.basename(input_path)
    return file_ingest_file(filename, input_path)

def ingest(input_path, wellbore_id=None, welllog_id=None):
    print("=====", input_path)
    print("--", wellbore_id)
    print('--', welllog_id)
    ori_file_id = __upload_file(input_path)
    results = convert_las_to_record(input_path, wellbore_id=wellbore_id, welllog_id=welllog_id, config_path=config_path)
    for item in results:
        wellbore_record = item['wellbore']
        wbid = wellbore_record.get_raw_data().get('id')
        result = search_query('osdu:wks:master-data--Wellbore:*', f'id: "{wbid}"', returnedFields=['id'])
        print("Search RESULT: ", wbid, result['totalCount'])
        if result['totalCount'] == 0:
            client.create_wellbore(wellbore_record)
        
        welllog_record = wlSvc.recognize_log_family(item['welllog'], config.data_partition_id)
        welllog_record.data['Datasets'] = [f'{ori_file_id}:']
        welllog_ids = client.post_welllog(welllog_record)
        welllog_id = welllog_ids[0] if welllog_ids is not None and len(welllog_ids) > 0 else None
        if welllog_id is None:
            raise Exception('Cannot create WellLog record')

        welllog_record = client.get_welllog_record(welllog_id)
        print(welllog_record.get_raw_data())
        client.add_welllog_data(item['welllog_data'], welllog_id)
def wbd_get_wellbore(wellbore_id):
    wellbore_record = client.get_wellbore_record(wellbore_id)
    return wellbore_record.get_raw_data()

def wbd_get_welllog(welllog_id):
    welllog_record = client.get_welllog_record(welllog_id)
    return welllog_record.get_raw_data()

def wbd_list_welllogs_of_wellbore(wellbore_id):
    result = search_query('osdu:wks:work-product-component--WellLog:*', f'data.WellboreID: "{wellbore_id}:"', returnedFields=['id'])
    if result['totalCount'] == 0:
        print("No dataset found")
        return
    output_format(result['results'])

def wbd_list_curves_of_welllog(welllog_id):
    result = search_query('osdu:wks:work-product-component--WellLog:*', f'id: "{welllog_id}"', returnedFields=['data.Curves'])
    if result['totalCount'] > 0:
        output_format(result['results'][0]['data']['Curves'], filteredFields=['CurveID', 'LogCurveFamilyID', 'CurveUnit'])
    else:
        print("No curves exist")

if args.print and args.path:
    logger.info(f"LAS path: {args.path}")
    print_las_header(args.path)
elif args.convert and args.path and args.well:
    logger.info(f'LAS path convert: {args.path}')
    #convert_las_to_json(args.path, wellbore_id=__get_wellbore_id(args.well), welllog_id=__get_welllog_id(args.dataset), config_path='config.json')
    print(convert_las_to_record(args.path, wellbore_id=__get_wellbore_id(args.well), welllog_id=__get_welllog_id(args.dataset), config_path='config.json'))

elif args.ingest and args.path:
    input_path = hdfs_download(args.path)

    print(f'LAS path ingest: {args.path} {args.well} {args.dataset}')
    if args.well and args.dataset:
        ingest(input_path, wellbore_id=__get_wellbore_id(args.well), welllog_id=__get_welllog_id(args.dataset))
    elif args.well is None and args.dataset is None:
        filename, _ = path.splitext(path.basename(args.path))
        _, _, _, well, dataset, _ = filename.split("_")
        well = re.sub(r"\s+", "-", well)
        dataset = re.sub(r"\s+", "-", dataset)
        wellbore_id = __get_wellbore_id(well)
        welllog_id = __get_welllog_id(f"{well}.{dataset}")
        ingest(input_path, wellbore_id=wellbore_id, welllog_id=welllog_id)

elif args.get:
    if args.well:
        print(json.dumps(wbd_get_wellbore(__get_wellbore_id(args.well))))
    elif args.dataset:
        print(json.dumps(wbd_get_welllog(__get_welllog_id(args.dataset))))
elif args.list_wells:
    output_format(search_kind("osdu:wks:master-data--Wellbore:*", returnedFields=['id', 'data.FacilityName'])['results'])
elif args.list_datasets and args.well:
    wbd_list_welllogs_of_wellbore(__get_wellbore_id(args.well))
elif args.list_curves and args.dataset:
    wbd_list_curves_of_welllog(__get_welllog_id(args.dataset))
elif args.delete and args.dataset:
    wbd_delete_welllog(__get_welllog_id(args.dataset))
elif args.export and args.dataset and args.out_file:
    if args.origin:
        welllog = wbd_get_welllog(__get_welllog_id(args.dataset))
        origin_file_id = welllog['data']['Datasets'][0][:-1]
        file_download_file(origin_file_id, args.out_file)
    else:
        curves = None if args.curves is None else args.curves.split(',')
        las_file = wlSvc.download_and_construct_las(config, __get_welllog_id(args.dataset), curves)
        with open(args.out_file, 'w') as f:
            las_file.write(f, version=2)
