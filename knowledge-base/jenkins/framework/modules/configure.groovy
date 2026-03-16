def run(Map config) {

    def pipeline = config.pipeline


    pipeline.echo "Building ${config.service}"

    config.global.version = pipeline.sh(
        script: "git rev-parse --short HEAD",
        returnStdout: true
    ).trim()

    pipeline.echo "Version detected: ${config.global.version}"

    pipeline.script {

        def str_folder = "${pipeline.env.WORKSPACE}${config.str_folder}"

        config.obj_Utilities.CreateFolders(str_folder)

        pipeline.sh """
            date >> ${str_folder}\\example.txt
        """
    }

}

return this