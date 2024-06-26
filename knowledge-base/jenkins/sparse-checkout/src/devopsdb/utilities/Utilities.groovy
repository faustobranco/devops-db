/** 
 * Example code for configuring a Shared Library in Groovy for Jenkins.
 * @author fausto.branco
 * @author https://devops-db.com/
 * @version 1.0
 * @since   2024-05-09 
*/
package devopsdb.utilities

class Utilities implements Serializable {

  def obj_Pipeline_Context
  def Utilities(obj_Context) {
    obj_Pipeline_Context = obj_Context
  }
  def CreateFolders(String str_structure){
    /**
    * Method for creating folder structures.
    * @param str_structure String - Full path of the folder structure to be created..
    * @return Nothing.
    * @exception IOException On input error.
    * @see IOException
    */
    if (str_structure.isEmpty()) {
      throw new Exception("str_structure parameter is Empty");
    }
    File directory = new File(str_structure);
    if (! directory.exists()){
      directory.mkdirs();
    }
  }

  def getEnv(key){
    return obj_Pipeline_Context.env[key]
  }

  def SparseCheckout(String str_gitUrl, String str_gitBranch, String str_path, String str_gitCredentials, String str_DestinationPath){
    /**
     * Method for doing Sparse Checkout from a Git repository.
     * @param str_gitUrl Full Git repository URL (git@ or https).
     * @param str_gitBranch String - Name of the Branch from which the checkout will be made.
     * @param str_path String - Path of the source folder (git repository) from which the sparse checkout will be performed.
     * @param str_gitCredentials String - ID of the credential (Jenkins) used to connect to Git.
     * @return None.
     * @exception IOException On input error.
     * @see IOException
     */
    obj_Pipeline_Context.checkout([$class: 'GitSCM',
            branches: [[name: "*/${str_gitBranch}"]],
            userRemoteConfigs: [[credentialsId: "${str_gitCredentials}",url: "${str_gitUrl}"]],
            doGenerateSubmoduleConfigurations: false,
            extensions: [
                    [$class: 'CloneOption', noTags: false,
                     shallow: false],
                    [$class: 'CheckoutOption', timeout: 180],
                    [$class: 'CleanCheckout'],
                    [$class: 'SubmoduleOption', disableSubmodules: false,
                     parentCredentials: true,
                     recursiveSubmodules: true,
                     reference: '',
                     trackingSubmodules: false],
                    [$class: 'RelativeTargetDirectory', relativeTargetDir: "${str_DestinationPath}"],
                    [$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: "${str_path}/*"]]]
            ]
    ])
  }
}