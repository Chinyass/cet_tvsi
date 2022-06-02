from .NSnmp import Snmp

class LTP:
    def __init__(self,ip,community):
        self.snmp = Snmp(ip,community)

    def func_chunks_generators(self,lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]
    
    def find_ont(self,hex_serial):
        dec_serial = self.convert_hex_serial_to_dec(hex_serial)
        return self.get_ont_all(dec_serial)

    def get_ont_all(self,dec_serial):
        if self.is_ont_online(dec_serial):
            if self.is_ont_activated(dec_serial):
                return {
                    'SERIAL' : self.get_ont_serial(dec_serial),
                    'PORT' : self.get_ont_port(dec_serial),
                    'ID' : self.get_ont_id(dec_serial),
                    'MODEL' : self.get_ont_model(dec_serial),
                    'FIRMWARE' : self.get_ont_firmware(dec_serial),
                    'TEMPLATE' : self.get_ont_template(dec_serial),
                    'OPTICAL_RX' : self.get_ont_optical_rx(dec_serial),
                    'OPTICAL_TX' : self.get_ont_optical_tx(dec_serial),
                    'USER' : self.get_ont_acs_user(dec_serial),
                    'LOGIN' : self.get_ont_acs_login(dec_serial),
                    'PASSWORD' : self.get_ont_acs_password(dec_serial),
                    'PROFILE' : self.get_ont_acs_profile(dec_serial),
                    'VOIP_ENABLE' : self.get_ont_voip_enable(dec_serial),
                    'VOIP_NUMBER' : self.get_ont_voip_number(dec_serial),
                    'VOIP_PASSWORD' : self.get_ont_voip_password(dec_serial),
                    'error' : '',
                }
            else:
                return {
                    'error': 'ont unactivated'
                }

        else:
            return {
                'error': 'ont offline'
            }

    def get_ont_voip_password(self,dec_serial):
        data = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.6.8.{dec_serial}')
        if data == 'NOSUCHOBJECT':
            return ''
        else:
            return data

    def set_ont_voip_password(self,dec_serial,value):
        return self.snmp.set_string(f'1.3.6.1.4.1.35265.1.22.3.15.1.6.8.{dec_serial}',value)

    def get_ont_voip_number(self,dec_serial):
        data = self.snmp.get( f'1.3.6.1.4.1.35265.1.22.3.15.1.5.8.{dec_serial}')
        if data == 'NOSUCHOBJECT':
            return ''
        else:
            return data
    def set_ont_voip_number(self,dec_serial,value):
        return self.snmp.set_string( f'1.3.6.1.4.1.35265.1.22.3.15.1.5.8.{dec_serial}',value)

    def get_ont_voip_enable(self,dec_serial):
        data = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.4.8.{dec_serial}')
        if data == 'NOSUCHOBJECT':
            return ''
        else:
            return data

    def set_ont_voip_enable(self,dec_serial,value):
        return self.snmp.set_string(f'1.3.6.1.4.1.35265.1.22.3.15.1.4.8.{dec_serial}',value)

    def get_ont_acs_profile(self,dec_serial):
        data = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.3.8.{dec_serial}')
        if data == 'NOSUCHOBJECT':
            return 'Not created'
        else:
            return data
    
    def set_ont_acs_profile(self,dec_serial,value):
        return self.snmp.set_unsigned(f'1.3.6.1.4.1.35265.1.22.3.15.1.3.8.{dec_serial}',value)

    def get_ont_template(self,dec_serial):
        id = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.4.1.43.1.8.{dec_serial}')
        data = self.snmp.get(f'.1.3.6.1.4.1.35265.1.22.3.24.1.1.2.{id}')
        if data == 'NOSUCHINSTANCE':
            return 'Not created'
        else:
            return data
    
    def set_ont_template(self,dec_serial,value):
        return self.snmp.set_unsigned(f'.1.3.6.1.4.1.35265.1.22.3.24.1.1.2.{id}')

    def get_ont_acs_password(self,dec_serial):
        data = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.12.8.{dec_serial}')
        if data == 'NOSUCHOBJECT':
            return 'Not created'
        else:
            return data
    
    def set_ont_acs_password(self,dec_serial,value):
        return self.snmp.set_string(f'1.3.6.1.4.1.35265.1.22.3.15.1.12.8.{dec_serial}',value)

    def get_ont_acs_login(self,dec_serial):
        data = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.11.8.{dec_serial}')
        print(data)
        if data == 'NOSUCHOBJECT':
            return 'Not created'
        else:
            return data
    
    def set_ont_acs_login(self,dec_serial,value):
        return self.snmp.set_string(f'1.3.6.1.4.1.35265.1.22.3.15.1.11.8.{dec_serial}',value)

    def get_ont_acs_user(self,dec_serial):
        data = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.2.8.{dec_serial}')
        if data == 'NOSUCHOBJECT':
            return 'Not created'
        else:
            return data
    
    def set_ont_acs_user(self,dec_serial,value):
        return self.snmp.set_string(f'1.3.6.1.4.1.35265.1.22.3.15.1.2.8.{dec_serial}',value)

    def get_ont_optical_tx(self,dec_serial):
        return self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.14.1.8.{dec_serial}')

    def get_ont_optical_rx(self,dec_serial):
        return self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.11.1.8.{dec_serial}')

    def get_ont_firmware(self,dec_serial):
        return self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.17.1.8.{dec_serial}')

    def get_ont_model(self,dec_serial):
        return self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.12.1.8.{dec_serial}')

    def get_ont_id(self,dec_serial):
        return self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.4.1.8.{dec_serial}')

    def get_ont_port(self,dec_serial):
        return self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.3.1.8.{dec_serial}')

    def is_ont_activated(self,dec_serial):
        status = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.5.1.8.{dec_serial}')
        if status == '7':
            return True
        else:
            return False

    def convert_hex_serial_to_dec(self,hex_serial):
        st= ''
        r = []
        serial = hex_serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        return '.'.join( list(map(lambda x: str(int(x,16)),r)) )

    def get_ont_serial(self,dec_serial):
        data = self.snmp.get_pysnmp(f'1.3.6.1.4.1.35265.1.22.3.1.1.2.1.8.{dec_serial}')
        return data[2:].upper()

    def is_ont_online(self,dec_serial):
        data = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.1.1.2.1.8.{dec_serial}')
        print(data)
        if 'NOSUCHINSTANCE' not in data:
            return True
        else:
            return False

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