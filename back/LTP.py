from NSnmp import Snmp
import time

class LTP:
    def __init__(self,ip,community):
        self.snmp = Snmp(ip,community)

    def func_chunks_generators(self,lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]
    
    def get_all_ont_online(self):
        data = self.snmp.walk_oid_value('1.3.6.1.4.1.35265.1.22.3.1.1.2.1.8')
        serials = ['.'.join(d[0].split('.')[-8:]) for d in data]
        return serials

    def walk_serial_value(self,oid):
        return list(
            map(
                lambda x: (x.oid.split('.')[-8:],x.value),self.snmp.walk(oid)
            )
        )
    
    
if __name__ == '__main__':
    l = LTP('10.3.0.26','private_set')