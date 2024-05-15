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
        stage('Environment') {
            agent {
                label 'docker'
            }
            steps {
                script {
                    def str_folder = "${env.WORKSPACE}/pipelines/resources/pip"
                    def str_folderCheckout = "/pip"
                    obj_Utilities.CreateFolders(str_folder)
                    obj_Utilities.SparseCheckout('git@gitlab.devops-db.internal:infrastructure/pipelines/resources.git',
                            'master',
                            str_folderCheckout,
                            'usr-service-jenkins',
                            str_folder)
                    sh 'sleep 1s'
                    sh "PIP_CONFIG_FILE=${str_folder}${str_folderCheckout}/pip-devops.conf pip install devopsdb"
                }
            }
        }
        stage('Script') {
            agent {
                label 'docker'
            }
            steps {
                script {
                    def str_folder = "${env.WORKSPACE}/pipelines/python/log"
                    def str_folderCheckout = "/python-log"
                    obj_Utilities.CreateFolders(str_folder)
                    obj_Utilities.SparseCheckout('git@gitlab.devops-db.internal:infrastructure/pipelines/tests.git',
                            'master',
                            str_folderCheckout,
                            'usr-service-jenkins',
                            str_folder)
                    sh "python3 ${str_folder}${str_folderCheckout}/python-log.py"
                }
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
