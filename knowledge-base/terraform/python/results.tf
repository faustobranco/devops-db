output "python_source_all" {
  value = data.external.python.result
}

output "python_source_var_source" {
  value = data.external.python.result.var_source
}

output "python_source_topic" {
  value = data.external.python.result.topic
}

locals {
  serverconfig = [
      for i in range(1, 10) : {
        instance_name = "${data.external.python.result.topic}-${data.external.python.result.var_source}-${format("%02s", i)}"
      }
  ]
}

output "servers" {
  value = local.serverconfig
}