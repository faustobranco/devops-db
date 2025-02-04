# pip install hvac
# https://pypi.org/project/hvac/


import hvac

VAULT_URL = 'http://vault.devops-db.internal:8200/'
VAULT_ROLE_ID = '2a89c925-62fc-44b7-fed5-d2de5e31cb69'
VAULT_SECRET_ID = 'f01e3323-ff2f-849d-e7a1-49805d2300e0'

client = hvac.Client(url=VAULT_URL)
ret_auth = client.auth.approle.login(VAULT_ROLE_ID, VAULT_SECRET_ID)
return_read_kv_1 = client.read('secret/data/infrastructure/jenkins/test-secret01')
print(return_read_kv_1)
print(return_read_kv_1['data']['data']['username'])
# usr-test01

print(return_read_kv_1['data']['data']['pwd'])
# 1234qwer

mount_point = 'secret'
secret_path = 'infrastructure/jenkins/test-secret01'
return_read_kv_2 = client.secrets.kv.v2.read_secret(path=secret_path, mount_point=mount_point)
print(return_read_kv_2['data']['data']['username'])
# usr-test01

print(return_read_kv_2['data']['data']['pwd'])
# 1234qwer


