@Library('devopsdb-global-lib') _

import devopsdb.utilities.Utilities
def obj_Utilities = new Utilities(this)

pipeline {
    agent {
        kubernetes {
            yaml GeneratePodTemplate('ansible_tests', 'registry.devops-db.internal:5000/ubuntu_ansible:2.16.8')
            retries 2
        }
    }
    options { timestamps ()
        skipDefaultCheckout(true)
    }
    environment {
        ANSIBLE_HOST_KEY_CHECKING = 'false' 
        host_group = 'infrastructure'
        host_tech = 'devops'
        host_service = 'cicd'
    }    
    stages {
        stage('Script') {
            steps {
                container('container-1') {
                    script {
                        def str_folder = "${env.WORKSPACE}/ansibles"
                        def str_folderCheckout = "/Inventory"
                        obj_Utilities.CreateFolders(str_folder)
                        obj_Utilities.SparseCheckout('git@gitlab.devops-db.internal:infrastructure/ansible/tests.git',
                                'master',
                                str_folderCheckout,
                                'usr-service-jenkins',
                                str_folder)
                    }
                }
            }
        }
        stage('Secrets') {
            steps {
                container('container-1') {
                    script {
                        def str_folder = "${env.WORKSPACE}/resources"
                        def str_folderCheckout = "/secrets"
                        obj_Utilities.CreateFolders(str_folder)
                        obj_Utilities.SparseCheckout('git@gitlab.devops-db.internal:infrastructure/ansible/tests.git',
                                'master',
                                str_folderCheckout,
                                'usr-service-jenkins',
                                str_folder)
                    }
                }
            }
        }
        stage('Ansible') {
            steps {
                container('container-1') {
                    script {
                        sh """ ansible-playbook ${env.WORKSPACE}/ansibles/Inventory/playbooks/dynamic_inventory.yaml\
                                             -i ${env.WORKSPACE}/ansibles/Inventory/global_hosts/inventory_json.py\
                                --vault-id prod@${env.WORKSPACE}/resources/secrets/.vault_password.sec """
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
