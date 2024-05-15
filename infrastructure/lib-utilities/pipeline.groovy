@Library('devopsdb-global-lib') _


import devopsdb.utilities.Utilities
import devopsdb.log.LogFormatter
import devopsdb.log.LogFormatterConstants
import devopsdb.log.Logger

def obj_Utilities = new Utilities(this)

LogFormatter obj_FormatterPipeline = new LogFormatter(LogFormatterConstants.const_Info, 'Logger Pipeline', false, '')
Logger obj_LogPipeline = new Logger(this, obj_FormatterPipeline)

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
                    obj_FormatterPipeline = new LogFormatter(LogFormatterConstants.const_Info, 'GeneratePassword', false, '')
                    obj_LogPipeline.info('Generating Password')
                    def str_Password = GeneratePassword(20, true)
                    obj_LogPipeline.info("Password: ${str_Password}")
                }
            }
        }
        stage('Validate') {
            agent {
            label 'docker'
            }       
            steps {
                sh 'ls -R'      
                sh 'sleep 1s'
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

