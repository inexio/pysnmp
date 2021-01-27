"""
Fetch two OID branches
++++++++++++++++++++++

Send a series of SNMP GETNEXT requests using the following options:

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to an Agent at demo-snmp.thola.io:161
* for two OIDs in string form
* stop when response OIDs leave the scopes of initial OIDs

Functionally similar to:

| $ snmpwalk -v2c -c public demo-snmp.thola.io 1.3.6.1.2.1.2.2.1.2 1.3.6.1.2.1.2.2.1.3

"""#
from pysnmp.hlapi import *

iterator = nextCmd(
    SnmpEngine(),
    CommunityData('public'),
    UdpTransportTarget(('demo-snmp.thola.io', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2')),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.3')),
    lexicographicMode=False
)

for errorIndication, errorStatus, errorIndex, varBinds in iterator:

    if errorIndication:
        print(errorIndication)
        break

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
        break

    else:
        for varBind in varBinds:
            print(' = '.join([ x.prettyPrint() for x in varBind ]))
