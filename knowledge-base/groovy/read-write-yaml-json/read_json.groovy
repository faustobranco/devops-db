import groovy.json.JsonSlurper
import groovy.json.JsonOutput

// #######################################################################################################################
// Read Json content

def str_Json = '''
{
  "version": 1,
  "group": "infrastructure",
  "tech": "dns",
  "service": "devops-db.info",
  "zones": [
    {
      "host": "ldap",
      "class": "IN",
      "type": "A",
      "destination": "172.21.5.150"
    },
    {
      "host": "registry",
      "class": "IN",
      "type": "A",
      "destination": "172.21.5.151"
    }
  ]
}
'''

def str_JsonFile = 'devops-db.info.json'
File obj_File = new File(str_JsonFile)

def map_Load_Json = new JsonSlurper().parseText(obj_File.getText())
//def map_Load_Json = new JsonSlurper().parseText(str_Json)

println('Resource: ' + map_Load_Json['group'] + '.' + map_Load_Json['tech'])
println('Domain: ' + map_Load_Json['service'])

map_Load_Json['zones'].each {item -> {
    println('Host: ' + item['host'] + ' - Destination: ' + item['destination'])
}}

// #######################################################################################################################
// Convert Map to Json
// prettyPrint a Json content

def map_Json = [
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

str_Json = JsonOutput.toJson(map_Json)
println(str_Json)

str_PP_Json = JsonOutput.prettyPrint(str_Json)
println(str_PP_Json)

// #######################################################################################################################
// Write Json Content
// It's better to use the contents of prettyPrint()

str_JsonFile = 'v2.devops-db.info.json'
File obj_JsonFile = new File(str_JsonFile)
obj_JsonFile.write(str_PP_Json)
