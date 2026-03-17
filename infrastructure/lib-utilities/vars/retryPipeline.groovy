def call(Map config = [:]) {

    int maxRetries = config.get('maxRetries', 3)
    int baseDelaySeconds = config.get('baseDelaySeconds', 60)

    int currentRetry = 0

    if (params.containsKey('RETRY_COUNT')) {
        currentRetry = params.RETRY_COUNT.toString().toInteger()
    }

    // Avoid retry on manual abort
    if (currentBuild.rawBuild.getResult().toString() == 'ABORTED') {
        echo "Build was aborted. Skipping retry."
        return
    }
    echo "Internal retry count: ${currentRetry}"

    if (currentRetry < maxRetries) {

        int nextRetry = currentRetry + 1
        int delaySeconds = baseDelaySeconds 

        currentBuild.displayName = "#${env.BUILD_NUMBER} (retry ${nextRetry})"

        echo "Retry ${nextRetry}/${maxRetries} in ${delaySeconds} seconds..."

        sleep time: delaySeconds, unit: 'SECONDS'

        // Propagate parameters
        def currentParams = params
            .findAll { key, value -> key != 'RETRY_COUNT' }
            .collect { key, value ->
                if (value instanceof Boolean) {
                    return booleanParam(name: key, value: value)
                } else {
                    return string(name: key, value: value.toString())
                }
            }

        currentParams += string(name: 'RETRY_COUNT', value: "${nextRetry}")

        build job: env.JOB_NAME,
              parameters: currentParams,
              wait: false

    } else {
        echo "Max retries reached (${maxRetries}). Not retrying."
    }
}