import pandas as pd
import yaml, json
import math

xlsx = pd.ExcelFile('mappings.xlsx', engine='openpyxl')
for sheet in xlsx.sheet_names:
  f_name = f'{sheet.lower()}_mappings.yaml'
  entries = xlsx.parse(sheet).to_dict('records')
  mappings = {}
  for entry in entries:
    if math.isnan(entry['STT']):
      print(f"skip {entry}")
      continue
    cache = { }
    for key in entry.keys():
      if key == 'prop' or key == 'STT':
        continue
      elif entry[key] and type(entry[key]) == str:
        if key == 'params':
          cache['params'] = json.loads(entry[key])
        elif key == 'value':
          cache = entry[key]
          break;
        elif key == 'array':
          cache = entry[key].split(',')
        else:
          cache[key] = entry[key]
    mappings[entry['prop']] = cache
  with open(f_name, 'w') as f:
    f.write(yaml.dump(mappings))
