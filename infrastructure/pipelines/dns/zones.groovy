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
        stage('Source') {
            when { not { changeRequest() } }
            steps {
                updateGitlabCommitStatus name: 'Validation', state: 'pending'
                cleanWs deleteDirs: true, disableDeferredWipeout: true
                git branch: 'master',
                    credentialsId: '4be56b6d-1679-4471-b845-a81423036205',
                    url: 'http://gitlab.devops-db.internal/infrastructure/pipelines/dns.git'
                sh 'pip install -r ${WORKSPACE}/requirements.txt'                    
                sh 'ls -lah ${WORKSPACE}'
            }
        }
        stage('Validation') {
            when { not { changeRequest() } }
            steps {
                sh 'printenv'
            }
        }
        stage('Build') {
            when { not { changeRequest() } }
            steps {
                sh 'sleep 3h'
            }
        }
        stage('Deploy') {
            when { branch 'master' }
            steps {
                updateGitlabCommitStatus name: 'Deploy', state: 'pending'
                sh 'printenv'
            }
        }
        stage('Cleanup') {
            steps {
                cleanWs deleteDirs: true, disableDeferredWipeout: true
                updateGitlabCommitStatus name: 'Cleanup', state: 'success'
            }
        }
    }
}