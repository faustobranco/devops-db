def call(Map config) {
    def templateName = config.template
    def slackWebhookURL = config.slackWebhookURL
    def data = config.data ?: [:]

    // Load template from resources
    def template = libraryResource("slack/${templateName}.json")

    // Replace variables
    def payload = renderTemplate(template, data)

    // Send to Slack
    def status = sh(
        script: """
            set +x
            curl -s -o /dev/null -w "%{http_code}" \
            -X POST -H 'Content-type: application/json' \
            --data '${payload}' \
            ${slackWebhookURL}
        """,
        returnStdout: true
    ).trim()

    if (status != "200") {
        echo "Slack notification failed with HTTP status: ${status}"
    }
}

def renderTemplate(String template, Map data) {
    def result = template

    data.each { key, value ->
        result = result.replace("\${${key}}", value.toString())
    }

    return result
}