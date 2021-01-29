"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'public'
  * over IPv4/UDP
  * to an Agent at demo-snmp.thola.io:161
  * for an instance of SNMPv2-MIB::sysDescr.0 MIB object
  * Based on asyncio I/O framework

Functionally similar to:

| $ snmpget -v1 -c public demo-snmp.thola.io SNMPv2-MIB::sysDescr.0

"""#
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


@asyncio.coroutine
def run():
    snmpEngine = SnmpEngine()

    iterator = getCmd(
        snmpEngine,
        CommunityData('public', mpModel=0),
        UdpTransportTarget(('demo-snmp.thola.io', 161)),
        ContextData(),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
    )

    errorIndication, errorStatus, errorIndex, varBinds = yield from iterator

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
        )
              )
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

    snmpEngine.transportDispatcher.closeDispatcher()


asyncio.get_event_loop().run_until_complete(run())
