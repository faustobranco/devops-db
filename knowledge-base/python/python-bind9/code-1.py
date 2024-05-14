filename = '/work/python/bind9/devops-db.info'
origin = 'devops-db.info'
hostname='ldap2'
ipaddr='172.21.5.153'
ttl = 7200

tmp_Zones = load_DNSZones(filename)

tmp_lst_Records = get_ARecords(tmp_Zones)
print(tmp_lst_Records)

#######################################################################################################################

tmp_obj_Records = load_ARecords(tmp_Zones, hostname)
if len(tmp_obj_Records) == 0:
    obj_Return = add_ARecords(tmp_obj_Records, ipaddr, ttl)
obj_Return = write_DNSZones(tmp_Zones)

tmp_lst_Records = get_ARecords(tmp_Zones)
print(tmp_lst_Records)


#######################################################################################################################

tmp_obj_Records = load_ARecords(tmp_Zones, 'test1')
if len(tmp_obj_Records) == 0:
    obj_Return = add_ARecords(tmp_obj_Records, '172.21.5.155', ttl)

tmp_obj_Records = load_ARecords(tmp_Zones, 'test2')
if len(tmp_obj_Records) == 0:
    obj_Return = add_ARecords(tmp_obj_Records, '172.21.5.156', ttl)

tmp_obj_Records = load_ARecords(tmp_Zones, 'test3')
if len(tmp_obj_Records) == 0:
    obj_Return = add_ARecords(tmp_obj_Records, '172.21.5.157', ttl)

obj_Return = write_DNSZones(tmp_Zones)

tmp_lst_Records = get_ARecords(tmp_Zones)
print(tmp_lst_Records)


#######################################################################################################################

obj_Return = remove_ARecords(tmp_Zones, 'ldap2')
obj_Return = remove_ARecords(tmp_Zones, 'test1')
obj_Return = remove_ARecords(tmp_Zones, 'test2')
obj_Return = remove_ARecords(tmp_Zones, 'test3')

obj_Return = write_DNSZones(tmp_Zones)

tmp_lst_Records = get_ARecords(tmp_Zones)
print(tmp_lst_Records)