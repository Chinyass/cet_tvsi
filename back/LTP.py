from NSnmp import Snmp
from pysnmp import hlapi
import time
import asyncio

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

    def get_rx_traffic_ont(self,dec_serial):
        a1 = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.3.10.1.6.1.8.{dec_serial}.1.1')
        start = time.time()
        time.sleep(12)
        a2 = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.3.10.1.6.1.8.{dec_serial}.1.1')
        end = time.time()
        rx = int( ( int(a2) - int(a1) ) / ( end - start ) ) * 8
        return rx

    def test(self):
        return self.snmp.walk_index_value_pysnmp('asd')

    def get_all_rx_traffic_ont(self,dec_serials):
        traffics = []
        for dec_serial in dec_serials:
            data = self.get_rx_traffic_ont(dec_serial)
            traffics.append( (dec_serial,data) )
        
        return traffics

async def gr(l,o):
    print( await l.get_rx_traffic_ont(o) )

if __name__ == '__main__':
    l = LTP('10.3.0.26','private_set')
    online = l.get_all_ont_online()[:5]
    start = time.time()
    ioloop = asyncio.get_event_loop()
    tasks = []
    for i in online:
        tasks.append( ioloop.create_task( gr(l,i) ) )
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()
    print(time.time() - start )