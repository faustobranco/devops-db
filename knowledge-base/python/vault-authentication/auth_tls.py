# pip install hvac
#
import hvac

#######################################################################################################################
### This code snippet only serves to remove an "Unverified HTTPS" warning because the certificate we use is self signed.
import urllib3
urllib3.disable_warnings()
#######################################################################################################################


VAULT_URL = 'https://vault.devops-db.internal:8200/'

client = hvac.Client(cert=('auth_vault_cert.pem',
                           'auth_vault_key.pem'),
                     url=VAULT_URL,
                     verify=False)
client.login("/v1/auth/cert/login")

print(client.is_authenticated())

mount_point = 'secret'
secret_path = 'infrastructure/jenkins/test-secret01'
return_read_kv_2 = client.secrets.kv.v2.read_secret(path=secret_path, mount_point=mount_point)
print(return_read_kv_2['data']['data']['username'])
print(return_read_kv_2['data']['data']['pwd'])

