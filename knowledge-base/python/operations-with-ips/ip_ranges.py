def fn_IP_Int(ip):
    h = list(map(int, ip.split(".")))
    return (h[0] << 24) + (h[1] << 16) + (h[2] << 8) + (h[3] << 0)

def fn_Int_IP(ip):
    return ".".join(map(str, [((ip >> 24) & 0xff), ((ip >> 16) & 0xff), ((ip >> 8) & 0xff), ((ip >> 0) & 0xff)]))


# List os Fake IPs
lst_Ips_to_Check = ['230.219.199.124', '194.179.131.102', '137.91.87.90', '98.37.134.83', '99.1.73.16', '79.32.206.156', '137.118.71.74', '228.152.130.69', '171.51.109.141', '6.112.94.147']

# IP ranges for blocking.
lst_RangeIps_to_Block = [{'Initial': '5.0.0.1', 'Final': '10.255.255.255'}, {'Initial': '50.0.0.1', 'Final': '126.255.255.255'}, {'Initial': '128.0.0.1', 'Final': '197.255.255.255'}]

# IP ranges to allow..
 lst_RangeIps_to_Allow = [{'Initial': '10.0.0.0', 'Final': '10.255.255.255'}, {'Initial': '172.16.0.0', 'Final': '172.31.255.255'}, {'Initial': '192.168.0.0', 'Final': '192.168.255.255'}]

#######################################################################################################################
# Transforms the string IPs (Octets) to Int in order to compare the IP in a range of IPs.

print('Cheking lst_RangeIps_to_Block')
for item_IP in lst_Ips_to_Check:
    for item_Range in lst_RangeIps_to_Block:
        if fn_IP_Int(item_IP) >= fn_IP_Int(item_Range['Initial']) and fn_IP_Int(item_IP) <= fn_IP_Int(item_Range['Final']):
            print('Checking IP: ' + item_IP + ' / Range: ' + item_Range['Initial'] + ' ~ ' + item_Range['Final'] + ': Found in the Range.')
        else:
            print('Checking IP: ' + item_IP + ' / Range: ' + item_Range['Initial'] + ' ~ ' + item_Range['Final'] + ': Not found in the Range.')

print('\n')
print('Cheking lst_RangeIps_to_Allow')
for item_IP in lst_Ips_to_Check:
    for item_Range in lst_RangeIps_to_Allow:
        if fn_IP_Int(item_IP) >= fn_IP_Int(item_Range['Initial']) and fn_IP_Int(item_IP) <= fn_IP_Int(item_Range['Final']):
            print('Checking IP: ' + item_IP + ' / Range: ' + item_Range['Initial'] + ' ~ ' + item_Range['Final'] + ': Found in the Range.')
        else:
            print('Checking IP: ' + item_IP + ' / Range: ' + item_Range['Initial'] + ' ~ ' + item_Range['Final'] + ': Not found in the Range.')


#######################################################################################################################
# Another example of how to use IPs in Integers is for sorting, then transforming the IPs from numbers to strings (octets) again.

lst_Ints = list(map(fn_IP_Int, lst_Ips_to_Check))
print(list(map(fn_Int_IP, sorted(lst_Ints))))

