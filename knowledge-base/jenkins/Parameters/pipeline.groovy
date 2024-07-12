pipeline {
    parameters {
        string (name: 'str_services', defaultValue:'infrastructure', description: 'Blueprint origin service.')
        choice (name: 'opt_action', choices: ['Deploy', 'Redeploy', 'Delete'], description: 'Action on the resource.')
        booleanParam (name: 'bol_verbose', defaultValue: false, description: 'Show logs with verbose.')
        text (name: 'txt_commitmessage', defaultValue: '''this is a multi-line\nstring parameter example\n''', description: 'Commit Message.')
        password (name: 'pwd_deploy', defaultValue: 'SECRET', description: 'Password for deployment.')                                
    }
    agent any

    stages {
        stage('Build Deploy') {
            when {
                expression { return params.opt_action == 'Deploy' }
            }            
            steps {
                script {
                    println 'Build Deploy'
                    println 'String Parameter: ' + params.str_services
                    println 'Multi Line Parameter: ' + params.txt_commitmessage
                    println 'Option Parameter: ' + params.opt_action
                    println 'Boolean Parameter: ' + params.bol_verbose
                    println 'Password Parameter: ' + params.pwd_deploy
                }
            }
        }
        stage('Build Redeploy') {
            when {
                expression { return params.opt_action == 'Redeploy' }
            }            
            steps {
                script {
                    println 'Build Redeploy'
                    println 'String Parameter: ' + params.str_services
                    println 'Multi Line Parameter: ' + params.txt_commitmessage
                    println 'Option Parameter: ' + params.opt_action
                    println 'Boolean Parameter: ' + params.bol_verbose
                    println 'Password Parameter: ' + params.pwd_deploy
                }
            }
        }
        stage('Delete') {
            when {
                expression { return params.opt_action == 'Delete' }
            }            
            steps {
                script {
                    println 'Delete'
                    println 'String Parameter: ' + params.str_services
                    println 'Multi Line Parameter: ' + params.txt_commitmessage
                    println 'Option Parameter: ' + params.opt_action
                    println 'Boolean Parameter: ' + params.bol_verbose
                    println 'Password Parameter: ' + params.pwd_deploy
                }
            }
        }
    }   
}