from prettytable import PrettyTable
import json

def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def prettyTable(alist, filteredFields=None):
    table = PrettyTable()
    if filteredFields:
        table.field_names = list(filter(lambda x: x in filteredFields, flatten_data(alist[0]).keys()))
    else:
        table.field_names = flatten_data(alist[0]).keys()
    for row in alist:
        frow = flatten_data(row)
        if filteredFields:
            items = list(filter(lambda item: item[0] in filteredFields, frow.items()))
            table.add_row([v for _,v in items])
        else:
            table.add_row([v for _,v in frow.items()])
    print(table)

def printJson(data, filteredFields=None):
    print(json.dumps(data))

def output_format(data, outputFn=prettyTable, filteredFields=[]):
    outputFn(data, filteredFields)

