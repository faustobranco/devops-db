import groovy.yaml.YamlBuilder
import groovy.yaml.YamlSlurper

def str_Yaml = '''
version: 1
group: infrastructure
tech: dns
service: devops-db.info
zones:
  - host: ldap
    class: IN
    type: A
    destination: 172.21.5.150
  - host: registry
    class: IN
    type: A
    destination: 172.21.5.151
'''

def str_YamlFile = 'devops-db.info.yaml'
File obj_File = new File(str_YamlFile)

def yaml_Load = new YamlSlurper().parseText(obj_File.getText())
//def yaml_Load = new YamlSlurper().parseText(str_Yaml)

println('Resource: ' + yaml_Load['group'] + '.' + yaml_Load['tech'])
println('Domain: ' + yaml_Load['service'])

yaml_Load['zones'].each {item -> {
    println('Host: ' + item['host'] + ' - Destination: ' + item['destination'])
}}


// #######################################################################################################################
// Convert Map to Json
// prettyPrint a Json content

def map_Yaml = [
        version: 1,
        group: "infrastructure",
        tech: "dns",
        service: "devops-db.info",
        zones: [[
                        host: "ldap",
                        class: "IN",
                        type: "A",
                        destination: "172.21.5.150"],
                [
                        host: "registry",
                        class: "IN",
                        type: "A",
                        destination: "172.21.5.151"
                ]
        ]
]
def obj_YamlBuilder = new YamlBuilder()
obj_YamlBuilder(map_Yaml)

str_Yaml = obj_YamlBuilder.toString()
println(str_Yaml)

// #######################################################################################################################
// Write Json Content
// It's better to use the contents of prettyPrint()

str_YamlFile = 'v2.devops-db.info.yaml'
File obj_YamlFile = new File(str_YamlFile)
obj_YamlFile.write(str_Yaml)

