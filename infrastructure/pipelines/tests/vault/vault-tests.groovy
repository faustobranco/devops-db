@Library('devopsdb-global-lib') _

import devopsdb.utilities.Utilities
def obj_Utilities = new Utilities(this)

def secrets = [[path: 'secret/infrastructure/jenkins/test-secret01', engineVersion: 2, secretValues: [[envVar: 'var_username', vaultKey: 'username'],[envVar: 'var_pwd', vaultKey: 'pwd']]]]

def configuration = [disableChildPoliciesOverride: false, skipSslVerification: true, timeout: 60, vaultCredentialId: 'vault-jenkins', vaultUrl: 'http://vault.devops-db.internal:8200']

pipeline {
    agent {
        kubernetes {
            yaml GeneratePodTemplate('1234-ABCD', 'registry.devops-db.internal:5000/ubuntu_ansible:2.16.8')
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
                    withVault([configuration: configuration, vaultSecrets: secrets]) {
                        sh 'echo $var_username > sys-user-account.txt'
                        sh 'echo $var_pwd >> sys-user-account.txt'
                        sh 'env'
                        sh 'echo ${username}'
                        sh 'echo ${pwd}'
                    }
                sh 'sleep 10m'
                }
            }
        }
    }
}
