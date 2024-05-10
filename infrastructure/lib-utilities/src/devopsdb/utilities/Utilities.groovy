/** 
 * Example code for configuring a Shared Library in Groovy for Jenkins.
 * @author fausto.branco
 * @author https://devops-db.com/
 * @version 1.0
 * @since   2024-05-09 
*/
package devopsdb.utilities

class Utilities implements Serializable {
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
}