def run(Map config) {

    def pipeline = config.pipeline

    def serviceName = config.service


    pipeline.echo "Building image for ${serviceName}"

    pipeline.sh """
    echo docker build -t registry/app-${serviceName}:${config.pipeline.env.BUILD_NUMBER} services/${serviceName}
    """


}
return this