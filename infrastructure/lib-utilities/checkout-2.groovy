@Library('devopsdb-global-lib') _

import devopsdb.utilities.Utilities
def obj_Utilities = new Utilities(this)

pipeline {
    agent {
        docker {
            image 'registry.devops-db.internal:5000/ubuntu_python:3.10.6'
            label 'docker'
            args '-u root'
        }
    }
    options { timestamps ()
        skipDefaultCheckout(true)
    }
    stages {
        stage('Source') {
            agent {
                label 'docker'
            }
            steps {
                script {
                    def str_folder = "${env.WORKSPACE}/NewFolder/Level1/Level2"
                    println(str_folder)
                    obj_Utilities.CreateFolders(str_folder)
                    obj_Utilities.SparseCheckout('git@gitlab.devops-db.internal:infrastructure/pipelines/lib-utilities.git',
                            'master',
                            '/src/devopsdb/utilities',
                            'usr-service-jenkins',
                            str_folder)
                }
            }
        }
        stage('Validation') {
            agent {
                label 'docker'
            }
            steps {
                sh 'ls -lahR ${WORKSPACE}'
            }
        }
        stage('Build') {
            agent {
                label 'docker'
            }
            steps {
                sh 'sleep 10s'
            }
        }
        stage('Cleanup') {
            agent {
                label 'docker'
            }
            steps {
                cleanWs deleteDirs: true, disableDeferredWipeout: true
            }
        }
    }
}
