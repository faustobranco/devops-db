import jsonschema
import yaml
import json
from datetime import datetime

str_DateTime = ''

with open('/work/python/bind9/blueprint/devops-db.info.json', 'r') as tmp_file:
    obj_schema = json.load(tmp_file)

with open('/work/python/bind9/blueprint/devops-db.info.yaml', 'r') as tmp_json_stream:
    try:
        json_data = yaml.full_load(tmp_json_stream)
    except yaml.YAMLError as exception:
        raise exception
try:
    obj_validator = jsonschema.Draft202012Validator(obj_schema, format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER)
    obj_errors = obj_validator.iter_errors(json_data)
    lst_errors = []
    for error in obj_errors:
        lst_errors.append(error)
except jsonschema.exceptions.ValidationError as obj_exceptions:
    print(obj_exceptions)

str_DateTime = datetime.now().strftime('%H:%M:%S')

if len(lst_errors) == 0:
    print(str_DateTime + ' - Blueprint OK.')
else:
    for item_error in lst_errors:
        print(str_DateTime + ' - Blueprint validation error: ' + item_error.message + ' / Reason: ' + str(item_error.schema) + ' / Where: ' + str(list(item_error.absolute_path)))
