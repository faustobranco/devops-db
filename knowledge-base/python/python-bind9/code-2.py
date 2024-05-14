str_filename = '/Work/Python/Bind9/devops-db.info'
obj_Zone = dns.zone.from_file(str_filename, os.path.basename(str_filename), relativize=False)

str_Zones = obj_Zone.to_text('devops-db.info', relativize=False, want_comments=True)

lst_Zones = str_Zones.splitlines()
print(lst_Zones)

for str_Line in lst_Zones:
    print(str_Line)

#######################################################################################################################

lst_Zones = ['devops-db.info. 7200 IN SOA ns1.devops-db.info. fausto.branco.devops-db.info. 2024042901 7200 3600 604800 7200 ; NegativeCacheTTL',
'devops-db.info. 7200 IN NS ns1.devops-db.info.',
'devops-db.info. 7200 IN NS 8.8.8.8.',
'devops-db.info. 7200 IN A 172.21.5.72',
'ldap.devops-db.info. 7200 IN A 172.21.5.150',
'ldap2.devops-db.info. 7200 IN A 172.21.5.153',
'ns1.devops-db.info. 7200 IN A 172.21.5.72',
'test1.devops-db.info. 7200 IN A 172.21.5.155',
'test2.devops-db.info. 7200 IN A 172.21.5.156',
'test3.devops-db.info. 7200 IN A 172.21.5.157']

str_Zones = '\n'.join(lst_Zones)

new_zone = dns.zone.from_text(str_Zones, relativize=False, origin='devops-db.info')
new_zone.to_file('devops-db.info', relativize=False, want_comments=True)