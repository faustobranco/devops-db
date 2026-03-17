@Library('devopsdb-global-lib') _

pipeline {

    agent any

    parameters {

        choice(
            name: 'PROJECT',
            choices: [
                'customers',
                'inventory',
                'orders',
                'payment',
                'reporting'
            ],
            description: 'Project to deploy'
        )

        string(
            name: 'APPLICATION_VERSION',
            defaultValue: '',
            description: 'Application version to deploy'
        )

        choice(
            name: 'ENVIRONMENT',
            choices: ['sandbox', 'staging', 'dev', 'prod'],
            description: 'Target environment'
        )
    }

    options {
        timestamps()
    }

    stages {

        stage('Initialize') {
            steps {
                script {
                    currentBuild.displayName = "${params.PROJECT} - ${params.APPLICATION_VERSION} - ${params.ENVIRONMENT}"
                    currentBuild.description = "Initializing"
                }
            }
        }

        stage('Validation') {
            steps {
                script {
                    currentBuild.description = "Validating"

                    if (!params.APPLICATION_VERSION?.trim()) {
                        env.ERROR_MESSAGE = "APPLICATION_VERSION cannot be empty"
                        error(env.ERROR_MESSAGE)
                    }

                    echo "Project: ${params.PROJECT}"
                    echo "Version: ${params.APPLICATION_VERSION}"
                    echo "Environment: ${params.ENVIRONMENT}"
                }
            }
        }

        stage('APPROVAL REQUIRED') {
            when {
                expression { params.ENVIRONMENT == 'prod' }
            }

            steps {
                script {

                    timeout(time: 30, unit: 'MINUTES') {

                        currentBuild.description = "Waiting for deploy approval"

                        withCredentials([string(credentialsId: 'slack-webhook-deployment', variable: 'SLACK_WEBHOOK_URL')]) {
                            def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")
                            def applicationVersion = params.APPLICATION_VERSION?.trim() ? 
                                                    params.APPLICATION_VERSION : 
                                                    "N/A"
                            
                            slackNotify(
                                template: "deployment_approval",
                                slackWebhookURL: SLACK_WEBHOOK_URL,
                                data: [
                                    version: applicationVersion,
                                    service: params.PROJECT,
                                    environment: params.ENVIRONMENT,
                                    urlPipeline: env.BUILD_URL,
                                    eventDate: timestamp,
                                    urlApproval: env.BUILD_URL + "input"

                                ]
                            )
                        }                

                        def approver = input(
                            message: """
                                Approval required.

                                Project: ${params.PROJECT}
                                Version: ${params.APPLICATION_VERSION}
                                Environment: ${params.ENVIRONMENT}

                                Do you want to continue with the deployment?
                                """,
                            ok: "Deploy",
                            submitter: "DeploymentApprovers,JenkinsAdmin",
                            submitterParameter: "APPROVER"
                        )

                        echo "Deployment approved by ${approver}"

                        println("Approved by ${approver}")

                    }

                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    currentBuild.description = "Deploying"

                    echo "Starting deployment..."

                    sh """
                        echo "Deploying ${params.PROJECT}"
                        echo "Version ${params.APPLICATION_VERSION}"
                        echo "Environment ${params.ENVIRONMENT}"
                    """

                }
            }
        }

    }

    post {

        success {
            echo "Deployment finished successfully"
            script {
                withCredentials([string(credentialsId: 'slack-webhook-deployment', variable: 'SLACK_WEBHOOK_URL')]) {
                    def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")
                    def applicationVersion = params.APPLICATION_VERSION?.trim() ? 
                                             params.APPLICATION_VERSION : 
                                             "N/A"
                    
                    slackNotify(
                        template: "deployment_success",
                        slackWebhookURL: SLACK_WEBHOOK_URL,
                        data: [
                            version: applicationVersion,
                            service: params.PROJECT,
                            environment: params.ENVIRONMENT,
                            urlPipeline: env.BUILD_URL,
                            eventDate: timestamp
                        ]
                    )
                }                

                currentBuild.description = "Service deployed successfully"
            }

        }

        failure {
            script {
                withCredentials([string(credentialsId: 'slack-webhook-deployment', variable: 'SLACK_WEBHOOK_URL')]) {
                    def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")
                    def applicationVersion = params.APPLICATION_VERSION?.trim() ? 
                                             params.APPLICATION_VERSION : 
                                             "N/A"
                    def errorMessage = env.ERROR_MESSAGE?.trim() ?
                                    env.ERROR_MESSAGE :
                                    "FAILED for any reason"
                    
                    slackNotify(
                        template: "deployment_failed",
                        slackWebhookURL: SLACK_WEBHOOK_URL,
                        data: [
                            version: applicationVersion,
                            service: params.PROJECT,
                            environment: params.ENVIRONMENT,
                            errorMessage: errorMessage,
                            urlPipeline: env.BUILD_URL,
                            eventDate: timestamp
                        ]
                    )
                }                

                currentBuild.description = "Deployed: Pipeline failed"
            }
        }

        aborted {
            echo "Pipeline aborted"
            script {
                currentBuild.description = "Pipeline aborted"
            }
        }

    }

}