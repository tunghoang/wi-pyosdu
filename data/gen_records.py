import pandas as pd
import json, copy, yaml, os


INPUT_FILE = 'input.xlsx'
SHEETS = ('Organisation', 'Basin', 'Field')
#SHEETS = ('Organisation', )

dirname = os.path.dirname(__file__)

_RECORD_MAPPINGS = yaml.safe_load(open(dirname + '/record_mappings.yaml'))

MAPPINGS = {
  'Organisation': yaml.safe_load(open(dirname + '/organisation_mappings.yaml')),
  'Field': yaml.safe_load(open(dirname + '/field_mappings.yaml')),
  'Basin': yaml.safe_load(open(dirname + '/basin_mappings.yaml'))
}

def normalize(string):
  return string.replace(" ", "-")

def gen_id(rtype, obj_id):
  if rtype == 'Field':
    return f'osdu:master-data--Field:{obj_id}'
  elif rtype == 'Organisation':
    return f'osdu:master-data--Organisation:{obj_id}'
  else:
    return f'osdu:master-data--{rtype}:{obj_id}'

def gen_organisation_id(org_id):
  return f'osdu:master-data--Organisation:{org_id}'

def gen_name_aliases(alias):
  return [{
    'AliasName': alias,
    'AliasNameTypeID': "osdu:reference-data--AliasNameType:UniqueIdentifier:"
  }]

def eval_mapping_list_entry(source, mapping_ent_list):
  output = [eval_mapping_entry(source, mapping_ent) for mapping_ent in mapping_ent_list]
  return output

def eval_mapping_entry(source, mapping_ent):
  if type(mapping_ent) == str:
    return mapping_ent
  
  if type(mapping_ent) == list:
    return eval_mapping_list_entry(source, mapping_ent)

  column = mapping_ent.get('column', None)
  if column is not None:
    return source[column]

  fn = mapping_ent.get('function', None)
  params = mapping_ent.get('params', [])
  params = list(map(lambda item: eval_mapping_entry(source,item), params))
  if fn is not None:
    return eval(fn)(*params)

  raise Error('No or Invalid mapping')
  
def eval_mapping(source, mappings, key):
  mapping_ent = mappings[key]
  return eval_mapping_entry(source, mapping_ent)

def deep_insert(obj, key, value):
  d = obj
  keys = key.split('.')
  for subkey in keys[:-1]:
    d[subkey] = d.get(subkey, {})
    d = d[subkey]
  d[keys[-1]] = value

def apply_mappings(source, dest, mappings):
  for prop in mappings:
    deep_insert(dest, prop, eval_mapping(source, mappings, prop))

def do_gen(record_type, df):
  table = df.to_dict('records')
  mappings = MAPPINGS[rtype]
  records = []
  for row in table:
    #record = copy.deepcopy(_RECORD)
    record = {}
    apply_mappings(None, record, _RECORD_MAPPINGS)
    apply_mappings(row, record, mappings)
    records.append(record)
  with open(f'{record_type}.json', 'w') as f:
    f.write(json.dumps(records))

xlsx = pd.ExcelFile(INPUT_FILE)

dfs = {sheet_name: xlsx.parse(sheet_name) for sheet_name in SHEETS }

for rtype in SHEETS:
  do_gen(rtype, dfs[rtype])
