@Library('devopsdb-global-lib') _
import devopsdb.utilities.Utilities   
def obj_Utilities = new Utilities()
pipeline {
    agent {
        docker {
            image 'ubuntu_python:3.10.6'
            label 'docker'
            args '-u root'
        }
    }
    options { timestamps () 
              skipDefaultCheckout(true)
            }
    stages {
        stage('Example_src') {
            agent {
            label 'docker'
            }      
            steps {
                script {      
                    def str_folder = "${env.WORKSPACE}/NewFolder/Level1/Level2"
                    println(str_folder)
                    obj_Utilities.CreateFolders(str_folder)
                }
            }
        }
        stage('Example_vars') {
            agent {
            label 'docker'
            }      
            steps {
                script {      
                    def str_Password = GeneratePassword(20, true)
                    println(str_Password)
                }
            }
        }
        stage('Validate') {
            agent {
            label 'docker'
            }       
            steps {
                sh 'ls -R'      
                sh 'sleep 10m'
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

