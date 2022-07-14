from .NSnmp import Snmp

class LTP:
    def __init__(self,ip,community):
        self.snmp = Snmp(ip,community)

    def func_chunks_generators(self,lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]
    
    def find_ont_by_user(self,user):
        users_list = self.get_ont_acs_user_all()
        user_info = tuple(filter(lambda x: x[1] == user,users_list))
        if user_info:
            dec_serial = user_info[0][0]
            data = self.get_ont_all(dec_serial)
            if data['error']:
                data['error'] = 'User found but ' + data['error']
                return data
            else:
                return data
        else:
            return { 'error' : 'User not found' }

    def find_ont(self,hex_serial):
        dec_serial = self.convert_hex_serial_to_dec(hex_serial)
        return self.get_ont_all(dec_serial)

    def get_ont_all(self,dec_serial):
        if self.is_ont_online(dec_serial):
            if self.is_ont_activated(dec_serial):
                rx = self.get_ont_optical_rx(dec_serial)
                tx = self.get_ont_optical_tx(dec_serial)
                return {
                    'SERIAL' : self.get_ont_serial(dec_serial),
                    'PORT' : self.get_ont_port(dec_serial),
                    'ID' : self.get_ont_id(dec_serial),
                    'MODEL' : self.get_ont_model(dec_serial),
                    'FIRMWARE' : self.get_ont_firmware(dec_serial),
                    'TEMPLATE' : self.get_ont_template(dec_serial),
                    'OPTICAL_RX' : 0 if 'no' in rx else rx,
                    'OPTICAL_TX' : 0 if 'no' in tx else tx,
                    'USER' : self.get_ont_acs_user(dec_serial),
                    'LOGIN' : self.get_ont_acs_login(dec_serial),
                    'PASSWORD' : self.get_ont_acs_password(dec_serial),
                    'PROFILE' : self.get_ont_acs_profile(dec_serial),
                    'VOIP_ENABLE' : self.get_ont_voip_enable(dec_serial),
                    'VOIP_NUMBER' : self.get_ont_voip_number(dec_serial),
                    'VOIP_PASSWORD' : self.get_ont_voip_password(dec_serial),
                    'TEMPLATES' : self.get_ont_all_templates(),
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
    
    def set_port_mapping(self,dec_serial,lanip,localport,outsideport,protocol='UDP'):
        in_external_port = self.snmp.set_2str_1int(
            f'1.3.6.1.4.1.35265.1.22.3.60.1.3.8.{dec_serial}.1',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.4.8.{dec_serial}.1',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.5.8.{dec_serial}.1',
            
            'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.PortMapping.11.ExternalPort',
            outsideport,
            '4'
        )
        print('in_external_port',in_external_port)
        internal_client = self.snmp.set_2str_1int(
            f'1.3.6.1.4.1.35265.1.22.3.60.1.3.8.{dec_serial}.2',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.4.8.{dec_serial}.2',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.5.8.{dec_serial}.2',
            
            'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.PortMapping.11.InternalClient',
            lanip,
            '4'
        )
        print('internal_client',internal_client)
        in_internal_port = self.snmp.set_2str_1int(
            f'1.3.6.1.4.1.35265.1.22.3.60.1.3.8.{dec_serial}.3',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.4.8.{dec_serial}.3',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.5.8.{dec_serial}.3',
            
            'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.PortMapping.11.InternalPort',
            localport,
            '4'
        )
        print('in_internal_port',in_internal_port)
        mapping_descr = self.snmp.set_2str_1int(
            f'1.3.6.1.4.1.35265.1.22.3.60.1.3.8.{dec_serial}.4',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.4.8.{dec_serial}.4',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.5.8.{dec_serial}.4',
            
            'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.PortMapping.11.PortMappingDescription',
            'tvsi',
            '4'
        )
        print('mapping_descr',mapping_descr)
        mapping_enable = self.snmp.set_2str_1int(
            f'1.3.6.1.4.1.35265.1.22.3.60.1.3.8.{dec_serial}.5',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.4.8.{dec_serial}.5',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.5.8.{dec_serial}.5',
            
            'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.PortMapping.11.PortMappingEnabled',
            '1',
            '4'
        )
        print('mapping_enable',mapping_enable)
        mapping_protocol = self.snmp.set_2str_1int(
            f'1.3.6.1.4.1.35265.1.22.3.60.1.3.8.{dec_serial}.6',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.4.8.{dec_serial}.6',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.5.8.{dec_serial}.6',
            
            'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.PortMapping.11.PortMappingProtocol',
            protocol,
            '4'
        )
        print('mapping_protocol',mapping_protocol)
        mapping_remote_host = self.snmp.set_2str_1int(
            f'1.3.6.1.4.1.35265.1.22.3.60.1.3.8.{dec_serial}.7',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.4.8.{dec_serial}.7',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.5.8.{dec_serial}.7',
            
            'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.PortMapping.11.RemoteHost',
            "0.0.0.0",
            '4'
        )
        print('mapping_remote_host',mapping_remote_host)
        out_external_port = self.snmp.set_2str_1int(
            f'1.3.6.1.4.1.35265.1.22.3.60.1.3.8.{dec_serial}.8',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.4.8.{dec_serial}.8',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.5.8.{dec_serial}.8',
            
            'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.PortMapping.11.X_ELTEX_RU_ExternalPortEnd',
            outsideport,
            '4'
        )
        print('out_external_port',out_external_port)
        out_internal_port = self.snmp.set_2str_1int(
            f'1.3.6.1.4.1.35265.1.22.3.60.1.3.8.{dec_serial}.8',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.4.8.{dec_serial}.8',
            f'1.3.6.1.4.1.35265.1.22.3.60.1.5.8.{dec_serial}.8',
            
            'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.PortMapping.11.X_ELTEX_RU_InternalPortEnd',
            localport,
            '4'
        )
        print('out_internal_port',out_internal_port)
        if all( 
                (
                    in_external_port[0],
                    internal_client[0],
                    in_internal_port[0],
                    mapping_descr[0],
                    mapping_enable[0],
                    mapping_protocol[0],
                    mapping_remote_host[0],
                    out_external_port[0],
                    out_internal_port[0]
                ) 
            ):
            return True
        else:
            return False



    def set_olt_save(self):
        return self.snmp.set_unsigned(f'1.3.6.1.4.1.35265.1.22.1.50.0',1)
    
    def set_ont_reconfigurate(self,dec_serial):
        return self.snmp.set_unsigned(f'1.3.6.1.4.1.35265.1.22.3.1.1.20.1.8.{dec_serial}',1)

    def set_acs_reconfigurate(self,dec_serial):
        return self.snmp.set_unsigned(f'1.3.6.1.4.1.35265.1.22.3.15.1.16.8.{dec_serial}',1)

    def set_ont_delete_user(self,dec_serial):
        data = self.snmp.set_unsigned(f'1.3.6.1.4.1.35265.1.22.3.15.1.20.8.{dec_serial}',1)
        return data

    def get_ont_voip_password(self,dec_serial):
        data = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.6.8.{dec_serial}')
        if data == 'NOSUCHOBJECT':
            return ''
        else:
            return data

    def get_ont_voip_server(self,dec_serial):
        return self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.15.1.10.8.{dec_serial}')
    
    def set_ont_voip_server(self,dec_serial,value):
        return self.snmp.set_string(f'1.3.6.1.4.1.35265.1.22.3.15.1.10.8.{dec_serial}',value)

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
        return self.snmp.set_string(f'1.3.6.1.4.1.35265.1.22.3.15.1.3.8.{dec_serial}',value)

    def get_ont_template(self,dec_serial):
        id = self.snmp.get(f'1.3.6.1.4.1.35265.1.22.3.4.1.43.1.8.{dec_serial}')
        data = self.snmp.get(f'.1.3.6.1.4.1.35265.1.22.3.24.1.1.2.{id}')
        if data == 'NOSUCHINSTANCE':
            return 'Not created'
        else:
            return data
    
    def get_ont_all_templates(self):
        data = self.snmp.walk_index_value('1.3.6.1.4.1.35265.1.22.3.24.1.1.2')
        dict_data = {}
        for t in data:
            dict_data[t[0]] = t[1]
        
        return dict_data

    def set_ont_template(self,dec_serial,value):
        return self.snmp.set_unsigned(f'.1.3.6.1.4.1.35265.1.22.3.4.1.43.1.8.{dec_serial}',int(value))

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

    def get_ont_acs_user_all(self):
        data = self.snmp.walk_oid_value(f'1.3.6.1.4.1.35265.1.22.3.15.1.2.8')
        return list(map(lambda x: ( '.'.join(x[0].split('.')[-8:]), x[1]),data))

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
    l = LTP('10.3.0.35','private_set')
    dec_serial = l.convert_hex_serial_to_dec('ELTX810000F4')
    
    print('PORT MAPPING: ',l.set_port_mapping(dec_serial,'192.168.1.4','8888','9090') )
    print(l.set_acs_reconfigurate(dec_serial))