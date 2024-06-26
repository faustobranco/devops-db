@Library('devopsdb-global-lib') _

import devopsdb.utilities.Utilities
def obj_Utilities = new Utilities(this)                        

pipeline {
    agent {
//        kubernetes {
//            yamlFile 'file-pod/resources/pods/file-pod.yaml'
//            retries 2
//        }
        kubernetes {
            yaml """
        apiVersion: v1
        kind: Pod
        metadata:
          labels:
            some-label: "pod-template-${env.BUILD_ID}"
        spec:
          containers:
          - name: container-1
            image: registry.devops-db.internal:5000/img-jenkins-devopsdb:2.0
            env:
            - name: CONTAINER_NAME
              value: "container-1"
            volumeMounts:
            - name: shared-volume
              mountPath: /mnt
            command:
            - cat
            tty: true
          - name: container-2
            image: ubuntu:22.04
            env:
            - name: CONTAINER_NAME
              value: "container-2"
            volumeMounts:
            - name: shared-volume
              mountPath: /mnt
            command:
            - cat
            tty: true
          - name: jnlp
            image: jenkins/jnlp-slave      
            env:
            - name: CONTAINER_NAME
              value: "container-2"
            volumeMounts:
            - name: shared-volume
              mountPath: /mnt
            command:
            - cat
            tty: true            
          volumes:
          - name: shared-volume
            emptyDir: {}            
        """
            retries 2
        }
    }
    options { timestamps ()
        skipDefaultCheckout(true)
    }
    stages {
        stage('Environment') {
            steps {
                container('container-1') {
                    script {
                        sh 'echo $CONTAINER_NAME > /mnt/shared_volume.txt'
                        def str_folder = "/mnt/pipelines/resources"
                        def str_folderCheckout = "/pip"
                        obj_Utilities.CreateFolders(str_folder)
                        sh 'sleep 10m'
                        obj_Utilities.SparseCheckout('git@gitlab.devops-db.internal:infrastructure/pipelines/resources.git',
                                'master',
                                str_folderCheckout,
                                'usr-service-jenkins',
                                str_folder)
                        sh 'sleep 1s'
                        sh "PIP_CONFIG_FILE=${str_folder}${str_folderCheckout}/pip-devops.conf pip install devopsdb"
                    }
                }
            }
        }
        stage('Script') {
            steps {
                container('container-1') {
                    script {
                        def str_folder = "/mnt/pipelines/python/log"
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
        stage('Run') {
            steps {
                container('container-2') {
                    script {
                        def str_folder = "/mnt/pipelines/python/log"
                        def str_folderCheckout = "/python-log"
                        sh "python3 ${str_folder}${str_folderCheckout}/python-log.py"
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
