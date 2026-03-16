def run(Map config) {

    def pipeline = config.pipeline


    pipeline.echo "Deploying ${config.service} to ${config.deployEnvironment}"

    pipeline.sh """
        echo "helm upgrade ${config.service} chart --set image.tag=${config.global.version}"
        sleep 1
    """
    if (config.containsKey("PROJECT")) {
        println("PROJECT: " + config.PROJECT)
    }

    if (config.containsKey("APPLICATION_VERSION")) {
        println("APPLICATION_VERSION: " + config.APPLICATION_VERSION)
    }
    if (config.containsKey("ENVIRONMENT")) {
        println("ENVIRONMENT: " + config.ENVIRONMENT)
    }

}
return this
