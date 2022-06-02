from NSnmp import Snmp

ips = [
    '10.9.0.20',
    '10.9.0.22',
    '10.9.0.25',
    '10.9.0.27'
]

olt_snmp = [ Snmp(ip,'private_set') for ip in ips ]
print(olt_snmp[0].walk(''))