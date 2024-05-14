import docker

str_Docker_URI = 'tcp://172.21.5.70:2375'
str_Container_Name = 'srv-jenkins-01'
str_Command = 'chown jenkins:jenkins /tmp/devops-db.info'
bol_Privileged = True
str_User = 'root'

obj_DockerClient = docker.DockerClient(base_url=str_Docker_URI)
obj_Container = obj_DockerClient.containers.get(str_Container_Name)

obj_Return = obj_Container.exec_run(str_Command, privileged=bol_Privileged, user=str_User)

print(obj_Return)
