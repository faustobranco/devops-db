import docker
import tarfile
import io
import os

str_Docker_URI = 'tcp://172.21.5.70:2375'
str_Container_Name = 'srv-jenkins-01'
str_Source_File = '/Users/fausto.branco/OneDrive/Work/Python/Bind9/devops-db.info'
str_Destination_Path = '/tmp/'

obj_DockerClient = docker.DockerClient(base_url=str_Docker_URI)
obj_Container = obj_DockerClient.containers.get(str_Container_Name)

obj_stream = io.BytesIO()
with tarfile.open(fileobj=obj_stream, mode='w|') as tmp_tar, open(str_Source_File, 'rb') as tmp_file:
    obj_info = tmp_tar.gettarinfo(fileobj=tmp_file)
    obj_info.name = os.path.basename(str_Source_File)
    tmp_tar.addfile(obj_info, tmp_file)

obj_Container.put_archive(str_Destination_Path, obj_stream.getvalue())