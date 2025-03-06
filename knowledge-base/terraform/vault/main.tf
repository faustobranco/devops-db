locals {
  VAULT_URL       = "https://vault.devops-db.internal:8200/"
  VAULT_ROLE_ID   = "166b7809-2fc6-1825-7620-f2dff60bcbb1"
  VAULT_SECRET_ID = "50558d2c-fb33-f81f-3441-b33413d5bbb4"
}

provider "vault" {
  address = local.VAULT_URL
  skip_child_token = true
  skip_tls_verify = true

  auth_login {
    path = "auth/approle/login"

    parameters = {
      role_id = local.VAULT_ROLE_ID
      secret_id = local.VAULT_SECRET_ID
    }
  }
}

data "vault_kv_secret_v2" "example" {
  mount = "secret"
  name  = "infrastructure/jenkins/test-secret01"
}

output "servers" {
  value = nonsensitive(data.vault_kv_secret_v2.example)
  sensitive = true
}

resource "local_file" "test_output" {
  content  = yamlencode(data.vault_kv_secret_v2.example)
  filename = "test_output.yaml"
}