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
        stage('Build') {
            steps {
                sh 'date >> data.txt'
                sh 'ls -lah'
            }
        }
        stage('Finish') {
            steps {
                sh 'ls -lah'
                sh 'cat data.txt'
                sh 'sleep 1'
            }
        }
        stage('Cleanup') {
            steps {
                cleanWs deleteDirs: true, disableDeferredWipeout: true
            }
        }        
    }
}