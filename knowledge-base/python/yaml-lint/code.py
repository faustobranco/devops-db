# https://pypi.org/project/yamllint/

from yamllint.config import YamlLintConfig
from yamllint import linter
from datetime import datetime

str_DateTime = ''

yaml_config = YamlLintConfig('extends: default')
obj_YamlLinter = linter.run(open('devops-db.info.yaml', "r"), yaml_config)

str_DateTime = datetime.now().strftime('%H:%M:%S')

lst_YamlLinter = []

for p in obj_YamlLinter:
    lst_YamlLinter.append({'level': p.level, 'desc': p.desc, 'line': p.line})

if len(lst_YamlLinter) == 0:
    print(str_DateTime + ' - Blueprint OK.')
else:
    for p in lst_YamlLinter:
        print(str_DateTime + ' - Blueprint linter validation ' + str(p['level']) + ' / Reason: ' + str(p['desc']) + ' / Where: Line ' + str(p['line']))