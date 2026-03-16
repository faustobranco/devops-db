@Library('devopsdb-global-lib') _
import devopsdb.utilities.Utilities
def obj_Utilities = new Utilities(this)

def run(pipeline, Map config) {

    config.global = config

    if (!config.stages) {
        error("Pipeline configuration error: 'stages' must be defined")
    }

    config.pipeline = pipeline
    config.obj_Utilities = new Utilities(pipeline)

    def modules = [:]

    // LOAD MODULES

    def files = pipeline.sh(
        script: "ls modules/*.groovy",
        returnStdout: true
    ).trim().split("\n")

    files.each { file ->
        def moduleName = file.tokenize("/").last().replace(".groovy","")
        modules[moduleName] = load file
    }

    // CHECKOUT

    pipeline.stage("Checkout") {
        pipeline.checkout pipeline.scm
    }

    // EXECUTOR

    def executeStage = { stageConfig ->

        def merged = [:]
        merged.putAll(config)
        merged.putAll(stageConfig)

        merged.global = config

        def moduleName = merged.stage

        if (!modules[moduleName]) {
            pipeline.error("Module '${moduleName}' not found")
        }

        merged.pipeline = pipeline
        merged.obj_Utilities = config.obj_Utilities

        def stageName = merged.name ?: "${moduleName}-${merged.service ?: UUID.randomUUID()}"

        pipeline.stage(stageName) {

            def runModule = {
                modules[moduleName].run(merged)
            }

            if (merged.node) {

                pipeline.node(merged.node) {

                    if (merged.container) {
                        pipeline.container(merged.container) {
                            runModule()
                        }
                    } else {
                        runModule()
                    }
                }
            } else {
                if (merged.container) {
                    pipeline.container(merged.container) {
                        runModule()
                    }
                } else {
                    runModule()
                }
            }
        }
    }

    // STAGE ORCHESTRATION

    config.stages.each { item ->

        if (item instanceof List) {

            def parallelStages = [:]

            item.each { stageConfig ->

                def name = stageConfig.name ?: "${stageConfig.stage}-${stageConfig.service ?: UUID.randomUUID()}"

                parallelStages[name] = {
                    executeStage(stageConfig)
                }

            }

            pipeline.stage("Parallel") {
                pipeline.parallel parallelStages
            }

        } else {

            executeStage(item)

        }

    }

}

return this