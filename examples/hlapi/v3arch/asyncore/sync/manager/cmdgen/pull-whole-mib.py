"""
Walk whole MIB
++++++++++++++

Send a series of SNMP GETNEXT requests using the following options:

* with SNMPv3, user 'usr-md5-none', MD5 authentication, no privacy
* over IPv4/UDP
* to an Agent at demo-snmp.thola.io:161
* for all OIDs in IF-MIB

Functionally similar to:

| $ snmpwalk -v3 -lauthPriv -u usr-md5-none -A authkey1 -X privkey1 demo-snmp.thola.io  IF-MIB::

"""#
from pysnmp.hlapi import *

iterator = nextCmd(
    SnmpEngine(),
    UsmUserData('usr-md5-none', 'authkey1'),
    UdpTransportTarget(('demo-snmp.thola.io', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('IF-MIB'))
)

for errorIndication, errorStatus, errorIndex, varBinds in iterator:

    if errorIndication:
        print(errorIndication)
        break

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        break

    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
