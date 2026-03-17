def call(Map config) {
    def templateName = config.template
    def slackWebhookURL = config.slackWebhookURL
    def data = config.data ?: [:]

    // Load template from resources
    def template = libraryResource("slack/${templateName}.json")

    // Replace variables
    def payload = renderTemplate(template, data)

    // Send to Slack
    sh(
        script: """
            curl -s -X POST -H 'Content-type: application/json' \
            --data '${payload}' \
            ${slackWebhookURL}
        """,
        label: "Send Slack notification"
    )
}

def renderTemplate(String template, Map data) {
    def result = template

    data.each { key, value ->
        result = result.replace("\${${key}}", value.toString())
    }

    return result
}