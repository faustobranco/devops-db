import com.github.dockerjava.api.DockerClient
import com.github.dockerjava.api.async.ResultCallback
import com.github.dockerjava.api.command.InspectContainerResponse
import com.github.dockerjava.api.model.Frame
import com.github.dockerjava.core.DefaultDockerClientConfig
import com.github.dockerjava.core.DockerClientBuilder
import com.github.dockerjava.core.DockerClientConfig
import com.github.dockerjava.okhttp.OkDockerHttpClient
import com.github.dockerjava.transport.DockerHttpClient

String str_Docker_URI = 'tcp://172.21.5.70:2375';
String str_Container_Name = 'test_python';
String[] lst_Command = new String[]{"/bin/bash", "-c", "counter=0; until [ \$counter -gt 5 ]; do echo \$(date '+%d/%m/%Y %H:%M:%S'); ((counter++)); sleep 1; done"};

class ret_DockerCommand {
    Boolean flg_Print = false;
//    Boolean flg_Logger = false;
    StringBuilder std_out = new StringBuilder();
    StringBuilder std_err = new StringBuilder();
    Boolean std_complete = false;

    def obj_Callback = new ResultCallback.Adapter<Frame>() {
        @Override
        void onNext(Frame object) {
            def str_tmp_result = new String(object.getPayload()).trim();
            std_out.append(str_tmp_result);
            if (flg_Print) { println(str_tmp_result) }
            super.onNext(object);
        }
        @Override
        void onError(Throwable throwable) {
            def str_tmp_result = new String(throwable as String).trim();
            std_err.append(str_tmp_result);
            if (flg_Print) { println(str_tmp_result) }
            super.onError(throwable);
        }
        @Override
        void onComplete() {
            std_complete=true;
            super.onComplete();
        }
    }
    ret_DockerCommand() {
    }
    ret_DockerCommand(Boolean Flag_Print) {
        this.flg_Print=Flag_Print;
    }
}

DockerClientConfig obj_dockerClientConfig = DefaultDockerClientConfig.createDefaultConfigBuilder()
        .withDockerHost(str_Docker_URI)
        .build();

DockerHttpClient obj_httpClient = new OkDockerHttpClient.Builder()
        .dockerHost(obj_dockerClientConfig.getDockerHost())
        .sslConfig(obj_dockerClientConfig.getSSLConfig())
        .build();

DockerClient obj_dockerClient = DockerClientBuilder.getInstance(obj_dockerClientConfig)
        .withDockerHttpClient(obj_httpClient)
        .build();

InspectContainerResponse obj_container = obj_dockerClient.inspectContainerCmd(str_Container_Name).exec();

try {
    final ret_DockerCommand obj_Output = new ret_DockerCommand(true);
    var obj_cmd_exec = obj_dockerClient
            .execCreateCmd(obj_container.getId())
            .withCmd(lst_Command)
            .withPrivileged(true)
            .withAttachStdout(true)
            .exec().getId()
    var obj_Return = obj_dockerClient
            .execStartCmd(obj_cmd_exec)
            .withTty(true)
            .exec(obj_Output.obj_Callback)
            .awaitCompletion()
    println("End");
}
catch (Exception obj_Exception) {
    println("Can't exec Docker command" + obj_Exception.toString());
}
