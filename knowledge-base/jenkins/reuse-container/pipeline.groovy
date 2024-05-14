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
        stage('Build') {
            agent {
                label 'docker'
            }      
            steps {
                sh 'date >> data.txt'
                sh 'ls -lah'
            }
        }
        stage('Finish') {
            agent {
            label 'docker'
            }       
            steps {
                sh 'ls -lah'
                sh 'cat data.txt'
                sh 'sleep 1'
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