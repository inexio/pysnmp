"""
Generic SNMPv2c TRAP
++++++++++++++++++++

Send SNMPv1 TRAP using the following options:

* SNMPv2c
* with community name 'public'
* over IPv4/UDP
* send TRAP notification
* with Uptime 12345
* with Generic Trap #1 (warmStart) and Specific Trap 0
* include managed object information '1.3.6.1.2.1.1.1.0' = 'my system'

Functionally similar to:

| $ snmptrap -v2c -c public demo-snmp.thola.io 12345 1.3.6.1.6.3.1.1.5.2 1.3.6.1.2.1.1.1.0 s "my system"

"""#
from pysnmp.hlapi.v1arch.asyncore import *


def cbFun(errorIndication, errorStatus, errorIndex, varBinds, **context):
    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


snmpDispatcher = SnmpDispatcher()

sendNotification(
    snmpDispatcher,
    CommunityData('public'),
    UdpTransportTarget(('demo-snmp.thola.io', 162)),
    'trap',
    # SNMPv2-MIB::sysUpTime.0 = 12345
    ('1.3.6.1.2.1.1.3.0', TimeTicks(12345)),
    # SNMPv2-SMI::snmpTrapOID.0 = SNMPv2-MIB::warmStart
    NotificationType(ObjectIdentity('SNMPv2-MIB', 'warmStart')),
    # SNMPv2-MIB::sysName.0
    ('1.3.6.1.2.1.1.1.0', OctetString('my system')),
    cbFun=cbFun,
    lookupMib=True
)

snmpDispatcher.transportDispatcher.runDispatcher()
