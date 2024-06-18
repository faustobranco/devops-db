pipeline {
    options { timestamps ()
        skipDefaultCheckout(true)
    }
    agent {
            label 'k8-agent'
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
