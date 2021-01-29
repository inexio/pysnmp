"""
SNMPv3: no auth, no privacy
+++++++++++++++++++++++++++

Send SNMP GET request using the following options:

* with SNMPv3, user 'usr-none-none', no authentication, no encryption
* over IPv4/UDP
* to an Agent at demo-snmp.thola.io:161
* for IF-MIB::ifInOctets.1 MIB object

Functionally similar to:

| $ snmpget -v3 -l noAuthNoPriv -u usr-none-none demo-snmp.thola.io IF-MIB::ifInOctets.1

"""#
from pysnmp.hlapi import *

iterator = getCmd(
    SnmpEngine(),
    UsmUserData('usr-none-none'),
    UdpTransportTarget(('demo-snmp.thola.io', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', 1))
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)

elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
