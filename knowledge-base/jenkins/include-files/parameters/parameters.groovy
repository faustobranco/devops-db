def getParameters(projectScript, versionScript) {

    return [

        [
            $class: 'CascadeChoiceParameter',
            choiceType: 'PT_SINGLE_SELECT',
            name: 'PROJECT',
            description: 'Select project',
            script: [
                $class: 'GroovyScript',
                script: [
                    $class: 'SecureGroovyScript',
                    script: projectScript,
                    sandbox: false
                ]
            ]
        ],

        [
            $class: 'CascadeChoiceParameter',
            choiceType: 'PT_SINGLE_SELECT',
            name: 'APPLICATION_VERSION',
            description: 'Select version',
            referencedParameters: 'PROJECT',
            script: [
                $class: 'GroovyScript',
                script: [
                    $class: 'SecureGroovyScript',
                    script: versionScript,
                    sandbox: false
                ]
            ]
        ],

        choice(
            name: 'ENVIRONMENT',
            choices: ['test','stage','prod'],
            description: 'Environment'
        )

    ]
}

return this