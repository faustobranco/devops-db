package devopsdb.utilities
class Utilities implements Serializable {
  def CreateFolders(String str_structure){
    if (str_structure.isEmpty()) {
      throw new Exception("str_structure parameter is Empty");
    }
    File directory = new File(str_structure);
    if (! directory.exists()){
      directory.mkdirs();
    }
  }
}