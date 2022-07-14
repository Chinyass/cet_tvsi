from easysnmp import Session
from typing import Tuple
import pysnmp.hlapi as pysnmp
from pysnmp.proto import rfc1902
import time

#class Session:
    #def __init__(hostname,community,version):
        #pass
    
class Snmp:
    def __init__(self,ip,community):
        self.session = Session(hostname=ip,community=community,version=2)
    
    def walk(self,oid):
        return list(
            map(
                lambda x: x.value,self.session.walk(oid)
            )
        )

    def walk_oid_value(self,oid):
        return list(
            map(
                lambda x: (x.oid,x.value),self.session.walk(oid)
            )
        )
    
    def walk_index(self,oid):
        return list(
            map(
                lambda x: x.oid.split('.')[-1],self.session.walk(oid)
            )
        )
    
    def walk_index_value(self,oid):
        return list(
            map(
                lambda x: (x.oid.split('.')[-1],x.value),self.session.walk(oid)
            )
        )
    
    def get(self,oid):
        return self.session.get(oid).value
    
    def get_pysnmp(self,oid):
        iterator = next(pysnmp.getCmd(
                                    pysnmp.SnmpEngine(),
                                    pysnmp.CommunityData(self.session.community),
                                    pysnmp.UdpTransportTarget( (self.session.hostname, '161') ),
                                    pysnmp.ContextData(),
                                    pysnmp.ObjectType(pysnmp.ObjectIdentity(oid) )
                        )
        )
        errIndication, errStatus, errIndex, vals = iterator
        if errIndication is not None:
            return str(errIndication)
        for name, val in vals:
            return str( val.prettyPrint() )
    
    def set_int(self,oid,value):
        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.session.community),
                                pysnmp.UdpTransportTarget( (self.session.hostname, '161') ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(oid),rfc1902.Integer(value),
                                ) ),
        )

        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            return (False,errorIndication)
        elif errorStatus:
            return (False,errorStatus)
        else:
            return (True,None)
    
    def set_unsigned(self,oid,value):
        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.session.community),
                                pysnmp.UdpTransportTarget( (self.session.hostname, '161') ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(oid),rfc1902.Unsigned32(value),
                                ) ),
        )

        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            return (False,errorIndication)
        elif errorStatus:
            return (False,errorStatus)
        else:
            return (True,None)
    
    def set_string(self,oid,value):
        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.session.community),
                                pysnmp.UdpTransportTarget( (self.session.hostname, '161') ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(oid),pysnmp.OctetString(value),
                                ) ),
        )

        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            return (False,errorIndication)
        elif errorStatus:
            return (False,errorStatus)
        else:
            return (True,None)
    
    def set_hexValue(self,oid,hex_vlan):
        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.session.community),
                                pysnmp.UdpTransportTarget( (self.session.hostname, '161') ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(oid),rfc1902.OctetString(hexValue=hex_vlan),
                                ) ),
        )

        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            return (False,errorIndication)
        elif errorStatus:
            return (False,errorStatus)
        else:
            return (True,None)
    
    def set_2str_1int(self,oid1,oid2,oid3,value1,value2,value3):
        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.session.community),
                                pysnmp.UdpTransportTarget( (self.session.hostname, '161') ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(oid1),rfc1902.OctetString(value1)),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(oid2),rfc1902.OctetString(value2)),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(oid3),rfc1902.Integer(value3)), 
                                ),
        )

        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            return (False,errorIndication)
        elif errorStatus:
            return (False,errorStatus)
        else:
            return (True,None)

    

    
if __name__ == '__main__':
    serial = 'ELTX83000CC4'
    snmp = Snmp('10.3.0.35','private_set')
    print(snmp.get_traffic_ont(serial))
    