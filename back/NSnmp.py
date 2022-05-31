#from easysnmp import Session
from typing import Tuple
import time

class Session:
    def __init__(self,hostname,community,version):
        pass
    
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
    
    
if __name__ == '__main__':
    serial = 'ELTX83000CC4'
    snmp = Snmp('10.3.0.35','private_set')
    print(snmp.get_traffic_ont(serial))
    