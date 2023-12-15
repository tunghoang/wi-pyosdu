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

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--print', action='store_true')
parser.add_argument('--convert', action='store_true')
parser.add_argument('--ingest', action='store_true')
parser.add_argument('--well')
parser.add_argument('--dataset')
parser.add_argument('--path')
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
        results.append({
            'wellbore':wellbore_record.get_raw_data(),
            'welllog':welllog_record.get_raw_data()
        })
    return results

def ingest(input_path, wellbore_id=None, welllog_id=None):
    logger.info(input_path, wellbore_id, welllog_id)
    results = convert_last_to_record(input_path, wellbore_id=wellbore_id, welllog_id=welllog_id, config_path=config_path)

if args.print and args.path:
    logger.info(f"LAS path: {args.path}")
    print_las_header(args.path)
elif args.convert and args.path and args.well:
    logger.info(f'LAS path convert: {args.path}')
    #convert_las_to_json(args.path, wellbore_id=__get_wellbore_id(args.well), welllog_id=__get_welllog_id(args.dataset), config_path='config.json')
    print(convert_las_to_record(args.path, wellbore_id=__get_wellbore_id(args.well), welllog_id=__get_welllog_id(args.dataset), config_path='config.json'))
elif args.ingest:
    logger.info(f'LAS path ingest: {args.path} {args.well} {args.dataset}')
    ingest(args.path, wellbore_id=__get_wellbore_id(args.well), welllog_id=__get_welllog_id(args.dataset))