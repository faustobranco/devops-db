@Library('devopsdb-global-lib') _

def default_maxRetries = 3
def default_baseDelaySeconds = 20

properties([
    parameters([
        string(name: 'ENV', defaultValue: 'dev'),
        booleanParam(name: 'RUN_TESTS', defaultValue: true),
        choice(name: 'REGION', choices: ['eu-central-1', 'eu-west-1', 'eu-north-1']),

        [$class: 'CascadeChoiceParameter',
            name: 'SERVICE',
            choiceType: 'PT_SINGLE_SELECT',
            script: [
                $class: 'GroovyScript',
                script: [script: "return ['payments','billing','orders']", sandbox: true],
                fallbackScript: [script: "return ['fallback']", sandbox: true]
            ]
        ],

        [$class: 'CascadeChoiceParameter',
            name: 'ENDPOINT',
            choiceType: 'PT_SINGLE_SELECT',
            referencedParameters: 'REGION',
            script: [
                $class: 'GroovyScript',
                script: [script: """
                    if (REGION == 'eu-central-1') {
                        return ['api.prod.local', 'api2.prod.local']
                    } else {
                        return ['api.dev.local', 'api2.dev.local']
                    }
                """, sandbox: true],
                fallbackScript: [script: "return ['fallback-endpoint']", sandbox: true]
            ]
        ]
    ])
])

pipeline {
    agent any

    stages {
        stage('Main') {
            steps {
                script {
                    echo "=== PARAMETERS PRINTS ==="
                    params.each { k, v ->
                        echo "${k} = ${v} (type=${v?.getClass()?.getName()})"
                    }                   
                    if (params.RETRY_COUNT.toInteger() < 2) {
                        error "Failing on purpose (simulate flaky dependency)"
                    }
                }
            }
        }
    }

    post {
        failure {
            retryPipeline(
                maxRetries: default_maxRetries,
                baseDelaySeconds: default_baseDelaySeconds
            )
        }
    }
}