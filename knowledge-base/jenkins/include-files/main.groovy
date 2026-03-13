@Library('devopsdb-global-lib') _

import devopsdb.utilities.Utilities
def obj_Utilities = new Utilities(this)        

def includes_steps = [:]                

node {
    // Garante que o repo existe no workspace
    checkout scm

    dir('include-files') {

        def projectScript = readFile('parameters/projectChoices.groovy')
        def versionScript = readFile('parameters/versionChoices.groovy')

        def parametersFile = load 'parameters/parameters.groovy'

        properties([
            parameters(
                parametersFile.getParameters(projectScript, versionScript)
            )
        ])
    }
}

pipeline {
    agent {
        kubernetes {
            yaml GeneratePodTemplate('1234-ABCD', 'registry.devops-db.internal:5000/img-jenkins-devopsdb:2.0')
            retries 2
        }
    }

    options { timestamps() }
    stages {

        stage('Load Includes') {
            steps {
                container('container-1') {
                    script {

                        includes_steps.stepOne = load "include-files/includes/stepOne.groovy"
                        includes_steps.stepTwo = load "include-files/includes/stepTwo.groovy"

                    }
                }
            }
        }

        stage('Run Steps') {
            steps {
                container('container-1') {
                    script {
                        includes_steps.stepOne.stepOne()
                        includes_steps.stepTwo.stepTwo()
                    }
                }
            }
        }

        stage('Example') {
            steps {
                echo "Project: ${params.PROJECT}"
                echo "Version: ${params.APPLICATION_VERSION}"
                echo "Environment: ${params.ENVIRONMENT}"
            }
        }
    }
}