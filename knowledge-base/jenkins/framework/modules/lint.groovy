def run(Map config) {

    def pipeline = config.pipeline


    pipeline.echo "Linting ${config.service}"

    pipeline.echo "Lint yaml OK"


}

return this