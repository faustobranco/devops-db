terraform {
  backend "pg" {
    conn_str = "postgres://terraform_backend:1Ov6DWitPlq*QyYL@postgresql.devops-db.internal:5432/db_terraform_backend?sslmode=disable"
    schema_name = "terraform_remote_state"
  }
}

variable "destination_email" { type = string }

