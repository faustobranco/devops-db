package devopsdb.docker

class DockerUtils implements Serializable {

    def obj_Pipeline_Context

    DockerUtils(obj_Context) {
        this.obj_Pipeline_Context = obj_Context
    }

    def dockerConfig(String BASE_IMAGE_NAME, String DEVOPSDB_DOCKER_REGISTRY, String ARGUMENTS = '', String LABEL = '', String CREDENTIAL_ID = '') {
        
        def config = [
            image: BASE_IMAGE_NAME, 
            registryUrl: "http://" + DEVOPSDB_DOCKER_REGISTRY,
            args: ARGUMENTS 
        ]
        
        if (LABEL && !LABEL.isEmpty()) {
            config.label = LABEL
        }
        
        if (CREDENTIAL_ID && !CREDENTIAL_ID.isEmpty()) {
            config.registryCredentialsId = CREDENTIAL_ID
        }
        
        return config
    }
}