from easysnmp import Session
from typing import Tuple
import time
from pysnmp import hlapi

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
    
    def walk_serial_value(self,oid):
        return list(
            map(
                lambda x: (x.oid.split('.')[-8:],x.value),self.session.walk(oid)
            )
        )
    
    def get(self,oid):
        return self.session.get(oid).value
    
    def get_rx_traffic_ont(self,dec_serial):
        return self.get(f'1.3.6.1.4.1.35265.1.22.3.3.10.1.6.1.8.{dec_serial}.1.1')
    
    def get_tx_traffic_ont(self,dec_serial):
        return self.get(f'1.3.6.1.4.1.35265.1.22.3.3.11.1.6.1.8.{dec_serial}.1.1')

    def convert_to_hex(self,bytes):
        s = ""
        for i in bytes:
            s += ("%0.2X" % ord(i))
        return s

    def convert_hex_to_dec(self,hexserial):
        r = []
        st = ''
        for i,num in enumerate(hexserial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        return '.'.join( list(map(lambda x: str(int(x,16)),r)) )

    def get_inform_from_dec_serial(self,dec_serial):
        SERIAL = self.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.2.1.8.{dec_serial}')
        if SERIAL == 'NOSUCHINSTANCE':
            SERIAL = 'OFFLINE'
        else:
            SERIAL = self.convert_to_hex(SERIAL)

        STATUS = self.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.5.1.8.{dec_serial}')
        if 'No' in STATUS:
            return {'STATUS':False}
        elif STATUS == '7':
            STATUS = 'ACTIVE'
        elif STATUS == '13':
            STATUS = 'UNACTIVATE'
        else:
            STATUS = 'UNKNOWN'
        
        PORT = self.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.3.1.8.{dec_serial}')
        if PORT == 'NOSUCHINSTANCE':
            PORT = 'OFFLINE'
        ID = self.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.4.1.8.{dec_serial}')
        if ID == 'NOSUCHINSTANCE':
            ID = 'OFFLINE'
        MODEL = self.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.12.1.8.{dec_serial}')
        if MODEL == 'NOSUCHINSTANCE':
            MODEL = 'OFFLINE'
        VERSION = self.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.17.1.8.{dec_serial}')
        if VERSION == 'NOSUCHINSTANCE':
            VERSION = 'OFFLINE'
        RX = self.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.11.1.8.{dec_serial}')
        if RX == 'NOSUCHINSTANCE':
            RX = 'OFFLINE'
        TX = self.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.14.1.8.{dec_serial}')
        if TX == 'NOSUCHINSTANCE':
            TX = 'OFFLINE'

        USER = self.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.2.8.{dec_serial}')
        USER = 'NOT CREATED' if USER == 'No Such Object currently exists at this OID' else USER
        LOGIN = self.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.11.8.{dec_serial}')
        LOGIN = 'NOT CREATED' if LOGIN == 'No Such Object currently exists at this OID' else LOGIN
        PASSWORD = self.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.12.8.{dec_serial}')
        PASSWORD = 'NOT CREATED' if PASSWORD == 'No Such Object currently exists at this OID' else PASSWORD
        PROFILE = self.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.3.8.{dec_serial}')
        PROFILE = 'NOT CREATED' if PROFILE == 'No Such Object currently exists at this OID' else PROFILE

        TEMPLATE_ID = self.get(f'.1.3.6.1.4.1.35265.1.22.3.4.1.43.1.8.{dec_serial}')
        TEMPLATE = self.get(f'.1.3.6.1.4.1.35265.1.22.3.24.1.1.2.{TEMPLATE_ID}')

        VOIP_ENABLE = self.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.4.8.{dec_serial}')
        VOIP_NUMBER = self.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.5.8.{dec_serial}')
        VOIP_PASSWORD = self.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.6.8.{dec_serial}')

        return {
            'SERIAL': SERIAL,
            'STATUS': STATUS,
            'PORT': PORT,
            'ID':ID,
            'MODEL':MODEL,
            'VERSION':VERSION,
            'RX':RX,
            'TX':TX,
            'USER':USER,
            'LOGIN':LOGIN,
            'PASSWORD':PASSWORD,
            'PROFILE':PROFILE,
            'TEMPLATE':TEMPLATE,
            'VOIP_ENABLE':VOIP_ENABLE,
            'VOIP_NUMBER':VOIP_NUMBER,
            'VOIP_PASSWORD':VOIP_PASSWORD
        }

    def get_inform_acs_user(self,search_personal):
        all_serial_and_user = self.walk_serial_value('1.3.6.1.4.1.35265.1.22.3.15.1.2.8')
        finded_user_dec_serial: Tuple[list,str] = list(filter(lambda x: x[1] == search_personal ,all_serial_and_user))
        if finded_user_dec_serial:
            finded_user_dec_serial = '.'.join( finded_user_dec_serial[0][0] )
        else:
            return False

        return self.get_inform_from_dec_serial(finded_user_dec_serial)
    
    def get_inform_ont(self,hexserial):
        hexserial = hexserial.replace('ELTX','454C5458')
        dec_serial = self.convert_hex_to_dec(hexserial)
        return self.get_inform_from_dec_serial(dec_serial)
    
    def get_traffic_ont(self,hexserial):
        hexserial = hexserial.replace('ELTX','454C5458')
        dec_serial = self.convert_hex_to_dec(hexserial)
        print(dec_serial)
        old_rx = self.get_rx_traffic_ont(dec_serial)
        #old_tx = self.get_tx_traffic_ont(dec_serial)
        start = int( time.time() )
        time.sleep(22)
        new_rx = self.get_rx_traffic_ont(dec_serial)
        #new_tx = self.get_tx_traffic_ont(dec_serial)
        end = int ( time.time() )

        rx = int( ( int(new_rx) - int(old_rx) ) / ( end - start ) ) * 8
        print(rx)
        tx = 0 #int( ( int(new_tx) - int(old_tx) ) / ( end - start ) ) * 8

        return (rx,tx)
    
    def get_traffic(self):
        old_rx = self.get('1.3.6.1.2.1.31.1.1.1.6.23')
        old_tx = self.get('1.3.6.1.2.1.31.1.1.1.10.23')
        start = int( time.time() )
        print(start)
        print('rx',old_rx)
        print('tx',old_tx)
        time.sleep(12)
        new_rx = self.get('1.3.6.1.2.1.31.1.1.1.6.23')
        new_tx = self.get('1.3.6.1.2.1.31.1.1.1.10.23')
        end = int ( time.time() )
        print(end)
        print('rx',new_rx)
        print('tx',new_tx)
        rx = int( ( int(new_rx) - int(old_rx) ) / ( end - start ) ) * 8
        tx = int( ( int(new_tx) - int(old_tx) ) / ( end - start ) ) * 8

        return (rx,tx)


if __name__ == '__main__':
    serial = 'ELTX83000CC4'
    snmp = Snmp('10.3.0.35','private_set')
    print(snmp.get_traffic_ont(serial))
    