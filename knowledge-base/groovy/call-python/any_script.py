import json

class Node_Folders():
    def sortPath(self, lst_Folders):
        return sorted(lst_Folders, key=lambda i: (self.fn_IP_Int(i['IP']), i['Path']))

    def filterPath(self, lst_Folders, lst_Filter):
        return list(filter(lambda d: d.get('Path') in lst_Filter, lst_Folders))

    def fn_IP_Int(self, str_IP: str):
        h = list(map(int, str_IP.split(".")))
        return (h[0] << 24) + (h[1] << 16) + (h[2] << 8) + (h[3] << 0)

def main():
    lst_dict_Data = [{'IP': '21.96.62.214', 'Link': False, 'Exists': False, 'Path': '/mnt/heapdump'},
                       {'IP': '21.96.62.214', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/saved_caches'},
                       {'IP': '21.96.62.214', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/hint'},
                       {'IP': '21.96.62.214', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/commitlog'},
                       {'IP': '253.102.1.103', 'Link': False, 'Exists': False, 'Path': '/mnt/heapdump'},
                       {'IP': '253.102.1.103', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/saved_caches'},
                       {'IP': '253.102.1.103', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/hint'},
                       {'IP': '253.102.1.103', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/commitlog'},
                       {'IP': '122.190.69.93', 'Link': False, 'Exists': False, 'Path': '/mnt/heapdump'},
                       {'IP': '122.190.69.93', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/saved_caches'},
                       {'IP': '122.190.69.93', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/hint'},
                       {'IP': '122.190.69.93', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/commitlog'},
                       {'IP': '174.40.30.197', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/saved_caches'},
                       {'IP': '174.40.30.197', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/hint'},
                       {'IP': '174.40.30.197', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/commitlog'},
                       {'IP': '226.14.168.44', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/saved_caches'},
                       {'IP': '226.14.168.44', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/hint'},
                       {'IP': '226.14.168.44', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/commitlog'},
                       {'IP': '222.53.239.60', 'Link': False, 'Exists': False, 'Path': '/mnt/heapdump'},
                       {'IP': '222.53.239.60', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/saved_caches'},
                       {'IP': '222.53.239.60', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/hint'},
                       {'IP': '222.53.239.60', 'Link': False, 'Exists': False, 'Path': '/mnt/cassandra/commitlog'}]
    obj_Node_Folders = Node_Folders()
    lst_tmp_Data = obj_Node_Folders.filterPath(lst_dict_Data, ['/mnt/cassandra/commitlog', '/mnt/cassandra/hint'])
    lst_tmp_Data = obj_Node_Folders.sortPath(lst_tmp_Data)
    json_lst_tmp_Data = json.dumps(lst_tmp_Data, indent=2)
    print(json_lst_tmp_Data)

if __name__ == "__main__":
   main()
   #globals()[sys.argv[1]](sys.argv[1])
   #python any_script.py main 1