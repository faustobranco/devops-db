# pip install hvac
# https://pypi.org/project/hvac/


import hvac

VAULT_URL = 'http://vault.devops-db.internal:8200/'
VAULT_ROLE_ID = '20745553-59b8-1499-4698-17489ffa1b18'
VAULT_SECRET_ID = 'ec5de6f2-9c30-ca12-2147-c27103758089'

client = hvac.Client(url=VAULT_URL)
ret_auth = client.auth.approle.login(VAULT_ROLE_ID, VAULT_SECRET_ID)

client.secrets.kv.v2.create_or_update_secret(
    mount_point='secret',
    path='infrastructure/jenkins/test-secret02',
    secret=dict(url='http://devops-db.internal/', token='1234567890qwertyuio'),
)

# {'request_id': '652ec9aa-06b1-734f-4574-0177ef2f8e8b', 'lease_id': '', 'renewable': False, 'lease_duration': 0, 'data': {'created_time': '2025-02-04T13:00:09.900091139Z', 'custom_metadata': None, 'deletion_time': '', 'destroyed': False, 'version': 1}, 'wrap_info': None, 'warnings': None, 'auth': None, 'mount_type': 'kv'}


return_read_kv_1 = client.read('secret/data/infrastructure/jenkins/test-secret02')
print(return_read_kv_1)
print(return_read_kv_1['data']['data']['url'])
# http://devops-db.internal/
 
print(return_read_kv_1['data']['data']['token'])
# 1234567890qwertyuio

