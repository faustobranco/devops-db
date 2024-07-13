@Library('devopsdb-global-lib') _

import devopsdb.utilities.Utilities
def obj_Utilities = new Utilities(this)                        

pipeline {
    agent {
        kubernetes {
            yaml GeneratePodTemplate('1234-ABCD', 'registry.devops-db.internal:5000/img-jenkins-devopsdb:2.0')
            retries 2
        }
    }
    options { timestamps ()
        skipDefaultCheckout(true)
    }
    stages {
        stage('Script') {
            steps {
                container('container-1') {
                    script {
                        def str_folder = "${env.WORKSPACE}/pipelines/python/log"
                        def str_folderCheckout = "/python-log"
                        obj_Utilities.CreateFolders(str_folder)
                        obj_Utilities.SparseCheckout('git@gitlab.devops-db.internal:infrastructure/pipelines/tests.git',
                                'master',
                                str_folderCheckout,
                                'usr-service-jenkins',
                                str_folder)
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                cleanWs deleteDirs: true, disableDeferredWipeout: true
            }
        }
    }
}
