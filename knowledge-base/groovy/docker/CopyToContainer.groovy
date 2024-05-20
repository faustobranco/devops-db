import com.github.dockerjava.api.DockerClient
import com.github.dockerjava.api.command.InspectContainerResponse
import com.github.dockerjava.core.DefaultDockerClientConfig;
import com.github.dockerjava.core.DockerClientBuilder
import com.github.dockerjava.core.DockerClientConfig
import com.github.dockerjava.transport.DockerHttpClient
import com.github.dockerjava.okhttp.OkDockerHttpClient
import org.apache.commons.compress.archivers.ArchiveStreamFactory
import org.apache.commons.compress.archivers.tar.TarArchiveEntry
import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream
import org.apache.commons.io.IOUtils

String str_Docker_URI = 'tcp://172.21.5.70:2375'
String str_Container_Name = 'test_python'
String str_Destination_TarFile = '/Users/fausto.branco/IdeaProjects/SparseCheckout/dns.tar'
String str_Destination_Path = '/tmp/test/'
List<String> lst_Source_File = ['/Users/fausto.branco/IdeaProjects/SparseCheckout/src/v2.devops-db.info.json']

Boolean CreateTarFile(String str_Destination_TarFile, List<String> lst_Source_File) {
    try {
        File str_TarFile = new File(str_Destination_TarFile)

        OutputStream obj_TarFile_Output = new FileOutputStream(str_TarFile);

        TarArchiveOutputStream obj_AOS = (TarArchiveOutputStream) new ArchiveStreamFactory().createArchiveOutputStream("tar", obj_TarFile_Output);

        for (String item_filePath : lst_Source_File) {
            File str_tmp_SourceFile = new File(item_filePath);
            TarArchiveEntry entry = new TarArchiveEntry(str_tmp_SourceFile);
            entry.setSize(str_tmp_SourceFile.length());
            obj_AOS.putArchiveEntry(entry);
            IOUtils.copy(new FileInputStream(str_tmp_SourceFile), obj_AOS);
            obj_AOS.closeArchiveEntry();
        }
        obj_AOS.close()
        obj_TarFile_Output.close();
        return true
    }
    catch(Exception obj_Exception) {
        println(obj_Exception.toString())
        return false
    }
}

Boolean CopyToContainer(String str_Docker_URI, String str_Container_Name, String str_Destination_TarFile, String str_Destination_Path) {
    try {
        File obj_TarFile = new File(str_Destination_TarFile)

        DockerClientConfig obj_dockerClientConfig = DefaultDockerClientConfig.createDefaultConfigBuilder()
                .withDockerHost(str_Docker_URI)
                .build();

        DockerHttpClient httpClient = new OkDockerHttpClient.Builder()
                .dockerHost(obj_dockerClientConfig.getDockerHost())
                .sslConfig(obj_dockerClientConfig.getSSLConfig())
                .build();

        DockerClient dockerClient = DockerClientBuilder.getInstance(obj_dockerClientConfig)
                .withDockerHttpClient(httpClient)
                .build();

        InspectContainerResponse container = dockerClient.inspectContainerCmd(str_Container_Name).exec();

        if (obj_TarFile.exists() && !obj_TarFile.isDirectory()) {
            FileInputStream tarStream = new FileInputStream(str_Destination_TarFile)
            dockerClient.copyArchiveToContainerCmd(container.getId())
                    .withRemotePath(str_Destination_Path)
                    .withTarInputStream(tarStream)
                    .exec();
        }
        return true
    }
    catch(Exception obj_Exception) {
        println(obj_Exception)
        return false
    }
}

if (CreateTarFile(str_Destination_TarFile, lst_Source_File)) {
    CopyToContainer(str_Docker_URI, str_Container_Name, str_Destination_TarFile, str_Destination_Path)
}

System.out.println("Files copied to container " + str_Container_Name);
