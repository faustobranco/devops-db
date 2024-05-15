withCredentials([usernamePassword(credentialsId: 'fixed',
                 usernameVariable: 'username',
                 passwordVariable: 'password')]){
    sh("git push http://$username:$password@git.corp.mycompany.com/repo")
}


withCredentials([sshUserPrivateKey(credentialsId: '<credential-id>', keyFileVariable: 'SSH_KEY')]) {
   sh("git push origin <local-branch>:<remote-branch>")
}

