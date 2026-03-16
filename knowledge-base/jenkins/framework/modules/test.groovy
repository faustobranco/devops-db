def run(Map config) {

    def pipeline = config.pipeline

    pipeline.echo "Running tests for ${config.service}"

    pipeline.sh """
        echo "Executing unit tests"
        sleep 1
    """

    pipeline.sh """
        ls -R "${pipeline.env.WORKSPACE}"
    """

    def str_folder = "${pipeline.env.WORKSPACE}${config.str_folder}"

    pipeline.sh """
        cat ${str_folder}\\example.txt
    """
}
return this