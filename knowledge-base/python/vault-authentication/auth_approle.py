# pip install hvac
#
#
# vault read auth/approle/role/jenkins-role/role-id
# Key        Value
# ---        -----
# role_id    2a89c925-62fc-44b7-fed5-d2de5e31cb69
#
#
# vault write -f auth/approle/role/jenkins-role/secret-id
# Key                   Value
# ---                   -----
# secret_id             f01e3323-ff2f-849d-e7a1-49805d2300e0
# secret_id_accessor    8562d2e5-b093-7ba2-5b7f-6e7eedd2461c
# secret_id_num_uses    0
# secret_id_ttl         0s
#
#
# vault kv put secret/infrastructure/jenkins/test-secret01 username="usr-test01" pwd="1234qwer"

import hvac

#######################################################################################################################
### This code snippet only serves to remove an "Unverified HTTPS" warning because the certificate we use is self signed.
import urllib3
urllib3.disable_warnings()
#######################################################################################################################

VAULT_URL = 'https://vault.devops-db.internal:8200/'
VAULT_ROLE_ID = '2a89c925-62fc-44b7-fed5-d2de5e31cb69'
VAULT_SECRET_ID = 'f01e3323-ff2f-849d-e7a1-49805d2300e0'

client = hvac.Client(url=VAULT_URL, verify=False)
client.auth.approle.login(role_id=VAULT_ROLE_ID,
                          secret_id=VAULT_SECRET_ID)

print(client.is_authenticated())

mount_point = 'secret'
secret_path = 'infrastructure/jenkins/test-secret01'
return_read_kv_2 = client.secrets.kv.v2.read_secret(path=secret_path, mount_point=mount_point)
print(return_read_kv_2['data']['data']['username'])
print(return_read_kv_2['data']['data']['pwd'])

