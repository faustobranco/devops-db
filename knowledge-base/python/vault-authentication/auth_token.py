# pip install hvac
#
#
# vault token create -policy=jenkins -period=24h
# Key                  Value
# ---                  -----
# token                hvs.CAESII56ND45A-xlSjhiNs4Z3UPGrSbCK3EYw4WtfGiaTCXHGh4KHGh2cy5RUjR3NW9iMktDOG1xM3p0ZGlmRDFvb1A
# token_accessor       OKAnjofeQOuc5dtLBs4rlBCA
# token_duration       24h
# token_renewable      true
# token_policies       ["default" "jenkins"]
# identity_policies    []
# policies             ["default" "jenkins"]
#
# vault token create -policy=jenkins -period=24h

import hvac
#######################################################################################################################
### This code snippet only serves to remove an "Unverified HTTPS" warning because the certificate we use is self signed.
import urllib3
urllib3.disable_warnings()
#######################################################################################################################

VAULT_URL = 'https://vault.devops-db.internal:8200/'
VAULT_TOKEN = 'hvs.CAESIIlShF_vvCkuVl15XvUFP6JCVrZvPaIGJT_ZpWxp77LKGh4KHGh2cy5RUUhZdHRnbTVxMUJhUUh4TFREcW5UYks'

client = hvac.Client(url=VAULT_URL, verify=False)
client.token = VAULT_TOKEN

print(client.is_authenticated())

mount_point = 'secret'
secret_path = 'infrastructure/jenkins/test-secret01'
return_read_kv_2 = client.secrets.kv.v2.read_secret(path=secret_path, mount_point=mount_point)
print(return_read_kv_2['data']['data']['username'])
print(return_read_kv_2['data']['data']['pwd'])

