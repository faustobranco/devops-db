## pip install docker
## https://docker-py.readthedocs.io/en/stable/images.html

import docker
import json

str_Registry = 'registry.devops-db.internal:5000'
str_Image = 'test_alpine'
str_Version = '1.0.1'
img_Tag = str_Registry + '/' + str_Image + ':' + str_Version

#######################################################################################################################################
### Using the client, it is not possible to stream the log in Build.
###   The only way is to use Low-level API

client = docker.APIClient(base_url='unix://var/run/docker.sock')
for line in client.build(path='/work/docker', rm=True,  tag=str_Image + ':' + str_Version):
    print(json.loads(line))

#######################################################################################################################################
obj_Return = docker.from_env().images.get(str_Image + ':' + str_Version).tag(img_Tag)

for line in client.push(img_Tag, stream=True, decode=True):
    print(line)

obj_Return = client.remove_image(image=img_Tag, force=True)
obj_Return = client.remove_image(image=str_Image + ':' + str_Version, force=True)
