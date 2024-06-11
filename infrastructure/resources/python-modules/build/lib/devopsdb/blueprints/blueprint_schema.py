import jsonschema
import yaml
import json
from datetime import datetime
from devopsdb.pipeline_utils import pipeline_logger
import os
import traceback

str_DateTime = ''
obj_logger = ''


def Validate_Schema(str_SchemaFilePath, str_YamlFilePath, str_SchemaFileContent='', str_YamlFileContent=''):
    try:
        obj_logger = pipeline_logger.CreateLogger('Schema')
        str_tmp_filename = os.path.basename(str_YamlFilePath)

        obj_logger.info('Starting Schema validation')
        obj_logger.info('Opening Schema - ' + str_tmp_filename)
        if str_SchemaFileContent != '':
            obj_tmp_SchemaFile = str_SchemaFileContent
        else:
            obj_tmp_SchemaFile = open(str_SchemaFilePath, "r")

        obj_schema = json.load(obj_tmp_SchemaFile)

        obj_logger.info('Opening Blueprint - ' + str_tmp_filename)
        if str_YamlFileContent != '':
            obj_tmp_YamlFile = str_YamlFileContent
        else:
            obj_tmp_YamlFile = open(str_YamlFilePath, "r")

        try:
            json_data = yaml.full_load(obj_tmp_YamlFile)
        except yaml.YAMLError as exception:
            raise exception

        try:
            obj_logger.info('Running Schema validation - ' + str_tmp_filename)
            obj_validator = jsonschema.Draft202012Validator(obj_schema, format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER)
            obj_errors = obj_validator.iter_errors(json_data)
            lst_errors = []
            for error in obj_errors:
                lst_errors.append(error)
        except jsonschema.exceptions.ValidationError as obj_exceptions:
            obj_logger.info('ValidationError  %s', obj_exceptions)
            exit()

        str_DateTime = datetime.now().strftime('%H:%M:%S')

        if len(lst_errors) == 0:
            return 0, [{'level': 0, 'desc': str_DateTime + ' - ' + str_tmp_filename + ' - Blueprint Schema validation OK.'}]
        else:
            ret_lst_YamlSchema = []
            for item_error in lst_errors:
                ret_lst_YamlSchema.append({'level':1, 'desc': str_DateTime + ' - ' + str_tmp_filename + ' - Blueprint schema validation error: ' + item_error.message + ' / Reason: ' + str(item_error.schema) + ' / Where: Line ' + str(list(item_error.absolute_path))})
            return 1, ret_lst_YamlSchema
    except Exception as obj_exceptions:
        lines = traceback.format_exception(type(obj_exceptions), obj_exceptions, obj_exceptions.__traceback__)
        obj_logger.debug(''.join(lines))
        obj_logger.critical('Validate_Schema Error: ' + str(obj_exceptions) + ' - Line: ' + str(obj_exceptions.__traceback__.tb_lineno))
        exit()
