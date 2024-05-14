import groovy.json.JsonSlurper

static void main(String[] args) {
    def cmd_out = new StringBuilder();
    def cmd_err = new StringBuilder();

    def cmdArray = ["python", "any_script.py"]
    def cmd = cmdArray.execute()

    cmd.consumeProcessOutput(cmd_out, cmd_err);
    cmd.waitForOrKill(1000)

    if (cmd_err.toString() == '') {
        def str_Return = cmd_out.toString()
        def obj_Json_parser = new JsonSlurper()
        def obj_json = obj_Json_parser.parseText(str_Return)
        obj_json.each {item -> {
            println(item)
        }}
    }
    else
    {
        println(cmd_err.toString())
    }

}
