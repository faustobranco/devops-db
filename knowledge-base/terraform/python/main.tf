data "external" "python" {
  program = ["python3", "${path.module}/example.py"]
  query = {
    topic_name = "DevOps-DB Example"
  }
}

