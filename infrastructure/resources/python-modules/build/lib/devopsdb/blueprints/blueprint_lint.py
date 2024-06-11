from yamllint.config import YamlLintConfig
from yamllint import linter
from datetime import datetime
from devopsdb.pipeline_utils import pipeline_logger
import os
from enum import Enum


class Lint_Level(Enum):
    """
    Lint_Level Enumerator.
    """
    OK = 0
    ERROR = 1
    WARNING = 2

obj_logger = ''
def lint(str_YamlFilePath, str_YamlFileContent=''):
    try:
        obj_logger = pipeline_logger.CreateLogger('Lint', pipeline_logger.LogLevel['debug'].value, '[%(asctime)s] - %(levelname)-8s - [%(name)-12s]: %(message)s', '%H:%M:%S')

        str_tmp_filename = os.path.basename(str_YamlFilePath)

        yaml_config = YamlLintConfig('extends: default')
        obj_logger.info('Starting Lint')
        obj_logger.info('Opening Blueprint - ' + str_tmp_filename)

        if str_YamlFileContent != '':
            obj_tmp_File = str_YamlFileContent
        else:
            obj_tmp_File = open(str_YamlFilePath, "r")
        obj_logger.info('Running Lint - ' + str_tmp_filename)
        obj_YamlLinter = linter.run(obj_tmp_File, yaml_config)

        str_DateTime = datetime.now().strftime('%H:%M:%S')

        lst_YamlLinter = []

        obj_logger.info('Exporting results - ' + str_tmp_filename)
        for p in obj_YamlLinter:
            lst_YamlLinter.append({'level': p.level, 'desc': p.desc, 'line': p.line})

        if len(lst_YamlLinter) == 0:
            return 0, [{'level': Lint_Level[str('OK').upper()].value, 'desc': str_DateTime + ' - ' + str_tmp_filename + ' - Blueprint Lint OK.'}]
        else:
            ret_lst_YamlLinter = []
            for p in lst_YamlLinter:
                ret_lst_YamlLinter.append({'level': Lint_Level[str(p['level']).upper()].value, 'desc': str_DateTime + ' - ' + str_tmp_filename + ' - Blueprint linter validation ' + str(p['level']) + ' / Reason: ' + str(p['desc']) + ' / Where: Line ' + str(p['line'])})
            return 1, ret_lst_YamlLinter
    except Exception as obj_exceptions:
        lines = traceback.format_exception(type(obj_exceptions), obj_exceptions, obj_exceptions.__traceback__)
        obj_logger.debug(''.join(lines))
        obj_logger.critical('Validate_Schema Error: ' + str(obj_exceptions) + ' - Line: ' + str(obj_exceptions.__traceback__.tb_lineno))
        exit()



