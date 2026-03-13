def stepTwo() {
    echo "Running step two"
    env.APP_NAME = params.PROJECT
    env.APP_VERSION = params.APPLICATION_VERSION
    env.APP_ENV = params.ENVIRONMENT
    sh 'env'
}

return this