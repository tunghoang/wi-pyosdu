from wi_pyosdu.client.File import *
from wi_pyosdu.client.Token import access_token
from wi_pyosdu.client.Search import *
from wi_pyosdu.client.Storage import *
from wi_pyosdu.models.SeismicBinGrid import SeismicBinGrid
from wi_pyosdu.models.SeismicTraceData import SeismicTraceData
from wi_pyosdu.models.SeismicHorizon import SeismicHorizon
from wi_pyosdu.models.SeismicFault import SeismicFault

import json
import re
import argparse
from os import path

from zipfile import ZipFile

from wi_common import *

parser = argparse.ArgumentParser()
parser.add_argument('--create', action="store_true")
parser.add_argument('--bin_grid_id')
parser.add_argument('--ingest', action="store_true")
parser.add_argument('--path')
parser.add_argument('--delete', action="store_true")
parser.add_argument('--list_all', action="store_true")
parser.add_argument('--list_bin_grid', action="store_true")
parser.add_argument('--list_trace_data', action="store_true")
parser.add_argument('--list_fault', action="store_true")
parser.add_argument('--list_horizon', action="store_true")
parser.add_argument('--trace_data_id')
parser.add_argument('--fault_id')
parser.add_argument('--horizon_id')
parser.add_argument('--export', action='store_true')
parser.add_argument('--outdir')
args = parser.parse_args()

def __get_bin_grid_id(bin_grid_id):
    return f'osdu:work-product-component--SeismicBinGrid:{bin_grid_id}'
def __get_trace_data_id(trace_data_id):
    return f'osdu:work-product-component--SeismicTraceData:{trace_data_id}'
def __get_horizon_id(horizon_id):
    return f'osdu:work-product-component--SeismicHorizon:{horizon_id}'
def __get_fault_id(fault_id):
    return f'osdu:work-product-component--SeismicFault:{fault_id}'

def delete_wpc(wpc_id):
    result = search_query('osdu:wks:work-product-component--*:*', f'id:"{wpc_id}"')
    if result['totalCount'] == 0:
        print(result)
        return
    wpc_record = result['results'][0]
    file_record_ids = wpc_record['data'].get('Datasets', [])
    for file_record_id in file_record_ids:
        file_delete_record(file_record_id[:-1])
    storage_delete_record(wpc_id)

def __unzipFile(filepath, outdir):
    with ZipFile(filepath) as zObject:
        zObject.extractall(path=outdir)

def export_wpc(wpc_id, outdir, unzip=False):
    result = search_query('osdu:wks:work-product-component--Seismic*:*', f'id:"{wpc_id}"', returnedFields=["id", "data.Datasets"])
    if result['totalCount'] == 0:
        print(result)
        raise Exception(f'Not found: {wpc_id}')
    print(result['results'])
    datasets = result['results'][0]['data']['Datasets']
    for ds in datasets:
        info = file_get_file(ds[:-1])
        filename = info['Name']
        file_download_file(ds[:-1], path.join(outdir, filename))
        if unzip:
            __unzipFile(path.join(outdir, filename), outdir)

def ingest_bin_grid(input_path, filename, bin_grid_id):
    result = search_query(
        'osdu:wks:dataset--File.Generic:*', 
        f'data.DatasetProperties.FileSourceInfo.Name:"{filename}"', 
        returnedFields=['id']
    )

    ori_file_id = None
    if result['totalCount'] == 0:
        ori_file_id = file_ingest_file(filename, args.path)
    else:
        ori_file_id = result['results'][0]['id']

    result = search_query('osdu:wks:work-product-component--SeismicBinGrid:*', f'data.BinGridName: "{bin_grid_id}"', returnedFields=['id'])
    bin_grid_record = SeismicBinGrid(bin_grid_id)
    bin_grid_record.data['Datasets'] = [f'{ori_file_id}:']
    storage_put_record(bin_grid_record)

def ingest_trace_data(input_path, filename, bin_grid_id, trace_data_id):
    result = search_query(
        'osdu:wks:work-product-component--SeismicBinGrid:*', 
        f'data.BinGridName: "{bin_grid_id}"', 
        returnedFields=['id']
    )
    if result['totalCount'] == 0:
        print(result)
        raise Exception(f'BinGrid {bin_grid_id} does not exist')
    
    result = search_query(
        'osdu:wks:dataset--File.Generic:*', 
        f'data.DatasetProperties.FileSourceInfo.Name:"{filename}"', 
        returnedFields=['id']
    )

    ori_file_id = None
    if result['totalCount'] == 0:
        ori_file_id = file_ingest_file(filename, args.path)
    else:
        ori_file_id = result['results'][0]['id']

    trace_data_record = SeismicTraceData(bin_grid_id, trace_data_id)
    trace_data_record.data['Datasets'] = [ f'{ori_file_id}:' ]
    storage_put_record(trace_data_record)
     
def ingest_horizon(input_path, filename, bin_grid_id, horizon_id):
    result = search_query(
        'osdu:wks:work-product-component--SeismicBinGrid:*', 
        f'data.BinGridName: "{bin_grid_id}"', 
        returnedFields=['id']
    )
    if result['totalCount'] == 0:
        raise Exception(f'BinGrid {bin_grid_id} does not exist')
    
    result = search_query(
        'osdu:wks:dataset--File.Generic:*', 
        f'data.DatasetProperties.FileSourceInfo.Name:"{filename}"', 
        returnedFields=['id']
    )

    ori_file_id = None
    if result['totalCount'] == 0:
        ori_file_id = file_ingest_file(filename, args.path)
    else:
        ori_file_id = result['results'][0]['id']

    horizon_record = SeismicHorizon(bin_grid_id, horizon_id)
    horizon_record.data['Datasets'] = [ f'{ori_file_id}:' ]
    storage_put_record(horizon_record)

def ingest_fault(input_path, filename, bin_grid_id, fault_id):
    result = search_query(
        'osdu:wks:work-product-component--SeismicBinGrid:*', 
        f'data.BinGridName: "{bin_grid_id}"', 
        returnedFields=['id']
    )
    if result['totalCount'] == 0:
        print(result)
        raise Exception(f'BinGrid {bin_grid_id} does not exist')
    
    result = search_query(
        'osdu:wks:dataset--File.Generic:*', 
        f'data.DatasetProperties.FileSourceInfo.Name:"{filename}"', 
        returnedFields=['id']
    )

    ori_file_id = None
    if result['totalCount'] == 0:
        ori_file_id = file_ingest_file(filename, args.path)
    else:
        ori_file_id = result['results'][0]['id']

    fault_record = SeismicFault(bin_grid_id, fault_id)
    fault_record.data['Datasets'] = [ f'{ori_file_id}:' ]
    storage_put_record(fault_record)

def list_bin_grid():
    result = search_kind('osdu:wks:work-product-component--SeismicBinGrid:*', returnedFields=["id", "data.BinGridName"])
    if result['totalCount'] == 0:
        print("No BinGrid exist")
        return
    output_format(result['results'])

def list_trace_data(bin_grid_id):
    result = search_query(
        'osdu:wks:work-product-component--SeismicTraceData:*', 
        f'data.BinGridID:"{bin_grid_id}:"',
        returnedFields=["id", "data.Name"]
    )
    if result['totalCount'] == 0:
        print(f"No TraceData found for BinGrid {bin_grid_id} exist")
        return
    output_format(result['results'])

def list_horizon(bin_grid_id):
    result = search_query(
        'osdu:wks:work-product-component--SeismicHorizon:*', 
        f'data.BinGridID:"{bin_grid_id}:"',
        returnedFields=["id", "data.Name"]
    )
    if result['totalCount'] == 0:
        print(f"No Horizon found for BinGrid {bin_grid_id} exist")
        return
    output_format(result['results'])

def list_fault(bin_grid_id):
    result = search_query(
        'osdu:wks:work-product-component--SeismicFault:*', 
        f'data.BinGridID:"{bin_grid_id}:"',
        returnedFields=["id", "data.Name"]
    )
    if result['totalCount'] == 0:
        print(f"No Fault found for BinGrid {bin_grid_id} exist")
        return
    output_format(result['results'])

def list_all(bin_grid_id):
    result = search_kind('osdu:wks:work-product-component--SeismicBinGrid:*', returnedFields=["id", "data.BinGridName"])
    if result['totalCount'] == 0:
        print(f"No Fault found for BinGrid {bin_grid_id} exist")
        return
    print(f'---------------------{bin_grid_id}--------------------')
    result = search_query(
        'osdu:wks:work-product-component--Seismic*:*', 
        f'data.BinGridID:"{bin_grid_id}:"',
        returnedFields=["id", "data.Name"]
    )
    if result['totalCount'] == 0:
        print(f"No data found for BinGrid {bin_grid_id} exist")
        return
    output_format(result['results'])

if args.ingest and args.path:
    filename, _ = path.splitext(path.basename(args.path))
    tokens = filename.split('_')

    if len(tokens) == 3:
        ingest_bin_grid(args.path, path.basename(args.path), tokens[2])
    elif len(tokens) == 4:
        ingest_trace_data(args.path, path.basename(args.path), tokens[2], tokens[3])
    elif len(tokens) == 5:
        if tokens[4] == 'Horizon':
            ingest_horizon(args.path, path.basename(args.path), tokens[2], tokens[3])
        elif tokens[4] == 'Fault':
            ingest_fault(args.path, path.basename(args.path), tokens[2], tokens[3])

elif args.list_bin_grid:
    list_bin_grid()

elif args.list_trace_data and args.bin_grid_id:
    list_trace_data(__get_bin_grid_id(args.bin_grid_id))

elif args.list_horizon and args.bin_grid_id:
    list_horizon(__get_bin_grid_id(args.bin_grid_id))

elif args.list_fault and args.bin_grid_id:
    list_fault(__get_bin_grid_id(args.bin_grid_id))

elif args.list_all and args.bin_grid_id:
    list_all(__get_bin_grid_id(args.bin_grid_id))

elif args.delete and args.bin_grid_id:
    delete_wpc(__get_bin_grid_id(args.bin_grid_id))

elif args.delete and args.trace_data_id:
    delete_wpc(__get_trace_data_id(args.trace_data_id))

elif args.delete and args.horizon_id:
    delete_wpc(__get_horizon_id(args.horizon_id))

elif args.delete and args.fault_id:
    delete_wpc(__get_fault_id(args.fault_id))

elif args.export and args.fault_id and args.outdir:
    export_wpc(__get_fault_id(args.fault_id), args.outdir)

elif args.export and args.horizon_id and args.outdir:
    export_wpc(__get_horizon_id(args.horizon_id), args.outdir)

elif args.export and args.bin_grid_id and args.outdir:
    export_wpc(__get_bin_grid_id(args.bin_grid_id), args.outdir, unzip=True)

elif args.export and args.trace_data_id and args.outdir:
    export_wpc(__get_trace_data_id(args.trace_data_id), args.outdir)

elif args.create and args.bin_grid_id:
    bin_grid_record = SeismicBinGrid(args.bin_grid_id)
    print(json.dumps(storage_put_record(bin_grid_record)))
