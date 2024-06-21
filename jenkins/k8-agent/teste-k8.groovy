pipeline {
    options { timestamps ()
        skipDefaultCheckout(true)
    }
    agent {
            label 'microk8-agent'
          }
    stages {    
        stage('Script') {
            steps {
                script {
                  sh 'env'
                       }
            }
        }
    }
}
