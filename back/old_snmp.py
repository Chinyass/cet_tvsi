import pysnmp.hlapi as pysnmp
import ipaddress
import sys
import os
import shutil
import time
import pprint
from pprint import pprint
from datetime import datetime
from pysnmp.proto import rfc1902

class Snmp:
    def __init__(self,ip,port,community,location='unknown'):
        self.ip = ip
        self.port = port
        self.community = community
        self.location = location

    def get_template_profile_name(self,id):
        if id == 'No SNMP response received before timeout':
           return 'unknown'
        OID = f'.1.3.6.1.4.1.35265.1.22.3.24.1.1.2.{id}'
        iterator = self._iterator_get(OID)
        errIndication, errStatus, errIndex, vals = iterator
        if errIndication is not None:
            return str(errIndication)
        for name, val in vals:
            return val.prettyPrint()
    
    def get_templates_list(self):
        OID = f'.1.3.6.1.4.1.35265.1.22.3.24.1.1.2'
        temp = list()
        result = []
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in pysnmp.bulkCmd(
                        pysnmp.SnmpEngine(),
                        pysnmp.CommunityData(self.community),
                        pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                        pysnmp.ContextData(),
                        0,50,
                        pysnmp.ObjectType(pysnmp.ObjectIdentity(OID)),
                        lexicographicMode=False
                        ):

            if errorIndication:
                return str(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                
                for vals in varBinds:
                    if isinstance(vals,tuple):
                        continue
                    temp.append(vals.prettyPrint()) 
        
                                    
        for i in temp:
          id = '.'.join(i.split('=')[0].lstrip().split('.')[-1:]).rstrip()
          names = i.split('=')[1].lstrip()
          result.append({id:names})

        return result


    def get_template_id(self,dec_serial):
        OID = f'.1.3.6.1.4.1.35265.1.22.3.4.1.43.1.8.{dec_serial}'

        iterator = self._iterator_get(OID)
        errIndication, errStatus, errIndex, vals = iterator
        if errIndication is not None:
            return str(errIndication)
        for name, val in vals:
            return val.prettyPrint()

    def set_template_profile(self,serial,id):

        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'.1.3.6.1.4.1.35265.1.22.3.4.1.43.1.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),rfc1902.Unsigned32(id)),
                                )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        success = False
        if errorIndication:
            print('template',errorIndication)
            success = True
        elif errorStatus:
            print('template',errorStatus)
            success = True
        else:
            print('template yep')
            success = True

        for name, val in vals:
            print(val.prettyPrint())
        return success
        
    def set_delete_user(self,serial):
        st=''
        r=[]
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
            st +=num
            if i%2 != 0:
               r.append(st)
               st = ''
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )
        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.20.8.{dec_serial}'
        
        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),rfc1902.Unsigned32(1) ),
                                )
        )

        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('delete user ',errorIndication)
            return False
        elif errorStatus:
            print('delete user',errorStatus)
            return False
        else:
            print('delete user true')
            return True
        return True

    def set_voip_enable(self,serial):
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.4.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),rfc1902.OctetString('Enabled')),
                                )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('voip enable ',errorIndication)
            return False
        elif errorStatus:
            print('voip enable',errorStatus)
            return False
        else:
            print('voip true')
            return True
        return True

    def set_voip_number(self,serial,number):
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.5.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),rfc1902.OctetString(number)),
                                )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('voip number ',errorIndication)
            return False
        elif errorStatus:
            print('voip number',errorStatus)
            return False
        else:
            print('voip nuber')
            return True
        return True

    def set_voip_sip_server(self,serial,ip):
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''

        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.10.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),rfc1902.OctetString(ip)),
                                )
        )

        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('voip sip server ',errorIndication)
            return False
        elif errorStatus:
            print('voip sip server',errorStatus)
            return False
        else:
            print('voip sip server')
            return True
        return True

    def set_voip_pass(self,serial,password):
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.6.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),rfc1902.OctetString(password)),
                                )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('voip pass ',errorIndication)
            return False
        elif errorStatus:
            print('voip pass',errorStatus)
            return False
        else:
            print('voip nuber')
            return True
        return True


    def get_null_acs_login(self):
        
        OID = '1.3.6.1.4.1.35265.1.22.3.15.1.2.8'
        temp = list()
        result = []
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in pysnmp.bulkCmd(
                        pysnmp.SnmpEngine(),
                        pysnmp.CommunityData(self.community),
                        pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                        pysnmp.ContextData(),
                        0,50,
                        pysnmp.ObjectType(pysnmp.ObjectIdentity(OID)),
                        lexicographicMode=False
                        ):

            if errorIndication:
                return str(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                
                for vals in varBinds:
                    if isinstance(vals,tuple):
                        continue
                    temp.append(vals.prettyPrint()) 
                                    
        for i in temp:
          serial = '.'.join(i.split('=')[0].lstrip().split('.')[-8:]).rstrip()
          personal = i.split('=')[1].lstrip() 
          result.append((serial,personal))       
        
        dec_serials = []
        for user in result:
            serial,personal = user
            #print(serial,personal)
            OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.11.8.{serial}'
            acs_user_login = self.func_get(OID)
            if acs_user_login == 'No Such Instance currently exists at this OID':
                continue
            if acs_user_login == "":
                print(serial,acs_user_login)
                OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.2.1.8.{serial}'
                exists_serial = self.func_get(OID)
                print(exists_serial)
                if exists_serial != 'No Such Instance currently exists at this OID':
                    exists_serial = exists_serial[2:].upper()
                    dec_serials.append(serial)

        res = []

        print(dec_serials)

        for dec_serial in dec_serials:
            print(dec_serial)
            if dec_serial:
                OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.2.1.8.{dec_serial}'
                exists_serial = self.func_get(OID)
                exists_serial = exists_serial[2:].upper()
                print(exists_serial)
            
                OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.5.1.8.{dec_serial}'
                status = self.func_get(OID)
                print(status)
            
                if status == '13':
                    return {'error':'status 13'}

                OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.3.1.8.{dec_serial}'
                port = self.func_get(OID)
                print(port)
                OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.4.1.8.{dec_serial}'
                serial_id = self.func_get(OID)
                print(serial_id)
                OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.12.1.8.{dec_serial}'
                model = self.func_get(OID)
            
                OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.17.1.8.{dec_serial}'
                version = self.func_get(OID)
                
                OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.11.1.8.{dec_serial}'
                rssi = self.func_get(OID)
            
                OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.14.1.8.{dec_serial}'
                rssitx = self.func_get(OID)
            
                OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.2.8.{dec_serial}' 
                acs_user_personal = self.func_get(OID)
            
                if acs_user_personal == 'No Such Object currently exists at this OID':
                    acs_user_personal = 'Not Created'

                OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.11.8.{dec_serial}'
                acs_user_login = self.func_get(OID)
            
                if acs_user_login == 'No Such Object currently exists at this OID':
                    acs_user_login = 'Not Created'
                OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.12.8.{dec_serial}'
                acs_user_password = self.func_get(OID)
            
                if acs_user_password == 'No Such Object currently exists at this OID':
                    acs_user_password = 'Not Created'

                OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.3.8.{dec_serial}'
                acs_user_profile = self.func_get(OID)

                

                if acs_user_profile == 'No Such Object currently exists at this OID':
                    acs_user_profile = 'Not Created'
                
                res.append( {
                    'error':False,
                    'ip':self.ip,
                    'port': port,
                    'id': serial_id,
                    'model':model,
                    'db':rssi,
                    'db_tx':rssitx,
                    'version':version,
                    'serial':exists_serial,
                    'acs_personal':acs_user_personal,
                    'acs_login':acs_user_login,
                    'acs_password':acs_user_password,
                    'acs_profile':acs_user_profile,
                    
                } )

            else:
                print('wtf')
        
        return res
    
    def get_inform_acs_user(self,search_personal):
        print('Ð¿Ð¾Ð»ÑƒÑ‡Ð°ÑŽ ÑÐµÑ€Ð¸Ð¹Ð½Ð¸ÐºÐ¸ Ð¸ Ð»Ð¸Ñ†ÐµÐ²Ñ‹Ðµ ÑÑ‡ÐµÑ‚Ð°',search_personal)
        OID = '1.3.6.1.4.1.35265.1.22.3.15.1.2.8'
        temp = list()
        result = []
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in pysnmp.bulkCmd(
                        pysnmp.SnmpEngine(),
                        pysnmp.CommunityData(self.community),
                        pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                        pysnmp.ContextData(),
                        0,50,
                        pysnmp.ObjectType(pysnmp.ObjectIdentity(OID)),
                        lexicographicMode=False
                        ):

            if errorIndication:
                return str(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                
                for vals in varBinds:
                    if isinstance(vals,tuple):
                        continue
                    temp.append(vals.prettyPrint()) 
                                    
        for i in temp:
          serial = '.'.join(i.split('=')[0].lstrip().split('.')[-8:]).rstrip()
          personal = i.split('=')[1].lstrip() 
          result.append((serial,personal))       
        
        dec_serial = self._compare(search_personal,result)
        print(dec_serial)
        if dec_serial:
        
            OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.2.1.8.{dec_serial}'
            exists_serial = self.func_get(OID)
            exists_serial = exists_serial[2:].upper()
        
            OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.5.1.8.{dec_serial}'
            status = self.func_get(OID)
         
            if status == '13':
                return {'error':'status 13'}

            OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.3.1.8.{dec_serial}'
            port = self.func_get(OID)
           
            OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.4.1.8.{dec_serial}'
            serial_id = self.func_get(OID)
           
            OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.12.1.8.{dec_serial}'
            model = self.func_get(OID)
          
            OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.17.1.8.{dec_serial}'
            version = self.func_get(OID)
            
            OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.11.1.8.{dec_serial}'
            rssi = self.func_get(OID)
          
            OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.14.1.8.{dec_serial}'
            rssitx = self.func_get(OID)
         
            OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.2.8.{dec_serial}' 
            acs_user_personal = self.func_get(OID)
          
            if acs_user_personal == 'No Such Object currently exists at this OID':
                acs_user_personal = 'Not Created'

            OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.11.8.{dec_serial}'
            acs_user_login = self.func_get(OID)
           
            if acs_user_login == 'No Such Object currently exists at this OID':
                acs_user_login = 'Not Created'
            OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.12.8.{dec_serial}'
            acs_user_password = self.func_get(OID)
           
            if acs_user_password == 'No Such Object currently exists at this OID':
                acs_user_password = 'Not Created'

            OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.3.8.{dec_serial}'
            acs_user_profile = self.func_get(OID)
           
            
            template_id = self.get_template_id(dec_serial)
            template = self.get_template_profile_name(template_id)
            template_names = self.get_templates_list()

            OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.4.8.{dec_serial}'
            acs_voip_enable = self.func_get(OID)

            OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.5.8.{dec_serial}'
            acs_voip_number = self.func_get(OID)

            OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.6.8.{dec_serial}'
            acs_voip_passw = self.func_get(OID)

            if acs_user_profile == 'No Such Object currently exists at this OID':
                acs_user_profile = 'Not Created'
            
            return {
                'error':False,
                'ip':self.ip,
                'port': port,
                'id': serial_id,
                'model':model,
                'db':rssi,
                'db_tx':rssitx,
                'version':version,
                'serial':exists_serial,
                'acs_personal':acs_user_personal,
                'acs_login':acs_user_login,
                'acs_password':acs_user_password,
                'acs_profile':acs_user_profile,
                'template':template,
                'template_names':template_names,
                'acs_voip_enable':acs_voip_enable,
                'acs_voip_number':acs_voip_number,
                'acs_voip_passw':acs_voip_passw

            }

        else:
            return {}

    def _compare(self,search_personal,users):
            for user in users:
                serial,personal = user
                if search_personal == personal:
                    return serial  

    def get_name(self):
        OID = '1.3.6.1.2.1.1.5.0' 
        iterator = self._iterator_get(OID)
        errIndication, errStatus, errIndex, vals = iterator
        if errIndication is not None:
            return str(errIndication)
        for name, val in vals:
            return val.prettyPrint()

    def get_sysDescr(self):
        OID = '1.3.6.1.2.1.1.1.0'
        iterator = self._iterator_get(OID)
        errIndication, errStatus, errIndex, vals = iterator
        if errIndication is not None:
            return str(errIndication)
        for name, val in vals:
            return val.prettyPrint()
            
    def get_traffic_rx(self,port):
        lport = port
        port = str(port + 48)
        OID = f'1.3.6.1.2.1.31.1.1.1.6.{port}'
        iterator = self._iterator_get(OID)
        errIndication, errStatus, errIndex, vals = iterator
        if errIndication is not None:
            #print(self.ip,'port',lport,'RX', errIndication,'returned 0')
            return str(errIndication)
        for name, val in vals:
            return val.prettyPrint()

    def get_traffic_tx(self, port):
        lport = port
        port = str(port + 48)
        OID = f'1.3.6.1.2.1.31.1.1.1.10.{port}'
        iterator = self._iterator_get(OID)
        errIndication, errStatus, errIndex, vals = iterator
        if errIndication is not None:
            #print(self.ip,'port',lport,'TX', errIndication,'returned 0')
            return str(errIndication)
        for name, val in vals:
            return val.prettyPrint()

    def set_CopyMesConf(self,myip):
        dirname = f'/tftp/{self.ip}'
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        name = f'MES-config.{datetime.strftime(datetime.now(), "%Y.%m.%d_%H_%M_%S")}.cfg'

        iterator = next(pysnmp.setCmd(
                                    pysnmp.SnmpEngine(),
                                    pysnmp.CommunityData(self.community),
                                    pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                    pysnmp.ContextData(),
                                    pysnmp.ObjectType(pysnmp.ObjectIdentity('1.3.6.1.4.1.89.87.2.1.3.1'),pysnmp.Integer(1) ),
                                    pysnmp.ObjectType(pysnmp.ObjectIdentity('1.3.6.1.4.1.89.87.2.1.7.1'),pysnmp.Integer(2) ),
                                    pysnmp.ObjectType(pysnmp.ObjectIdentity('1.3.6.1.4.1.89.87.2.1.8.1'),pysnmp.Integer(3) ),
                                    pysnmp.ObjectType(pysnmp.ObjectIdentity('1.3.6.1.4.1.89.87.2.1.9.1'),pysnmp.IpAddress(f'{myip}') ),
                                    pysnmp.ObjectType(pysnmp.ObjectIdentity('1.3.6.1.4.1.89.87.2.1.11.1'),pysnmp.OctetString(name) ),
                                    pysnmp.ObjectType(pysnmp.ObjectIdentity('1.3.6.1.4.1.89.87.2.1.17.1'),pysnmp.Integer(4) ),
                                 )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print(errorIndication)
            
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                
        else:
            pass   
        time.sleep(1)
        shutil.move(os.path.abspath(f"/tftp/{name}"), os.path.abspath(f'{dirname}/{name}'))

    def get_sysUpTime(self):
        OID = '1.3.6.1.2.1.1.3.0'
        iterator = self._iterator_get(OID)
        errIndication, errStatus, errIndex, vals = iterator
        for name, val in vals:
            return val.prettyPrint()

    def set_switchPort(self,port,status):
        OID = '1.3.6.1.2.1.2.2.1.7.{}'.format(str(port))

        if status == 'on':
            status_int = 1
        elif status == 'off':
            status_int = 2
        else:
            status_int = 'err'

        iterator = self._iterator_set(OID,status_int)
        errIndication, errStatus, errIndex, vals = iterator
        return f'Port:{port} Mode:{status}'


    def get_OntChannel13(self):
        serials = list(map(lambda x: x[2:].upper() ,self._get_OntSerials()))
        statuses = self._get_OntStateState()
        ports = self._get_OntPorts()
        
        lser = len(serials)
        lstats = len(statuses)
        lports = len(ports)

        equipment = dict()

        bol = lser == lstats and lser == lports

        if bol:
            for i in range(lser):
                if statuses[i] == '13':
                    equipment[serials[i]] = {
                        'port':ports[i],
                        'name':serials[i].replace('454C5458','ELTX')
                    }

        return equipment
    def func_get(self,OID):
        iterator = self._iterator_get(OID)
        errIndication, errStatus, errIndex, vals = iterator
        if errIndication is not None:
            return str(errIndication)
        for name, val in vals:
            return val.prettyPrint()

    def get_OntChannel7_One(self,serial):
        
        r = []
        st = ''
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''

        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )
        print(dec_serial)
        OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.2.1.8.{dec_serial}'
        exists_serial = self.func_get(OID)
        print(exists_serial)
        if exists_serial == 'No Such Instance currently exists at this OID' or exists_serial == 'No SNMP response received before timeout':
            return {'error':'Not found'}

        exists_serial = exists_serial[2:].upper()
        print(exists_serial)
        OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.5.1.8.{dec_serial}'
        status = self.func_get(OID)
        print(status)
        if status == '13':
            return {'error':'status 13'}

        OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.3.1.8.{dec_serial}'
        port = self.func_get(OID)
        print(port)
        OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.4.1.8.{dec_serial}'
        serial_id = self.func_get(OID)
        print(serial_id)
        OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.12.1.8.{dec_serial}'
        model = self.func_get(OID)
        print(model)
        OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.17.1.8.{dec_serial}'
        version = self.func_get(OID)
        print(version)
        OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.11.1.8.{dec_serial}'
        rssi = self.func_get(OID)
        print(rssi)
        OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.14.1.8.{dec_serial}'
        rssitx = self.func_get(OID)
        print(rssitx)
        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.2.8.{dec_serial}' 
        acs_user_personal = self.func_get(OID)
        print(acs_user_personal)
        if acs_user_personal == 'No Such Object currently exists at this OID':
            acs_user_personal = 'Not Created'

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.11.8.{dec_serial}'
        acs_user_login = self.func_get(OID)
        print(acs_user_login)
        if acs_user_login == 'No Such Object currently exists at this OID':
            acs_user_login = 'Not Created'
        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.12.8.{dec_serial}'
        acs_user_password = self.func_get(OID)
        print(acs_user_password)
        if acs_user_password == 'No Such Object currently exists at this OID':
            acs_user_password = 'Not Created'

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.3.8.{dec_serial}'
        acs_user_profile = self.func_get(OID)
        print(acs_user_profile)
        
        template_id = self.get_template_id(dec_serial)
        template = self.get_template_profile_name(template_id)
        template_names = self.get_templates_list()

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.4.8.{dec_serial}'
        acs_voip_enable = self.func_get(OID)

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.5.8.{dec_serial}'
        acs_voip_number = self.func_get(OID)

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.6.8.{dec_serial}'
        acs_voip_passw = self.func_get(OID)

        if acs_user_profile == 'No Such Object currently exists at this OID':
            acs_user_profile = 'Not Created'
        
        return {
            'error':False,
            'port': port,
            'id': serial_id,
            'model':model,
            'db':rssi,
	        'db_tx':rssitx,
            'version':version,
            'serial':serial,
            'acs_personal':acs_user_personal,
            'acs_login':acs_user_login,
            'acs_password':acs_user_password,
            'acs_profile':acs_user_profile,
	        'template':template,
            'template_names':template_names,
             'acs_voip_enable':acs_voip_enable,
             'acs_voip_number':acs_voip_number,
             'acs_voip_passw':acs_voip_passw

        }	


    def _iterator_get(self,OID):
        iterator = next(pysnmp.getCmd(
                                    pysnmp.SnmpEngine(),
                                    pysnmp.CommunityData(self.community),
                                    pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                    pysnmp.ContextData(),
                                    pysnmp.ObjectType(pysnmp.ObjectIdentity(OID) )
                        )
        )
        return iterator
    def _iterator_set(self, OID, status):
        iterator = next(pysnmp.setCmd(
                                    pysnmp.SnmpEngine(),
                                    pysnmp.CommunityData(self.community),
                                    pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                    pysnmp.ContextData(),
                                    pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),pysnmp.Integer(status) )
                                 )
        )
        return iterator

    
    def get_rssi(self,serial):
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        rssi = ''
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'1.3.6.1.4.1.35265.1.22.3.1.1.11.1.8.{dec_serial}'

        iterator = self._iterator_get(OID)
        errIndication, errStatus, errIndex, vals = iterator
        if errIndication is not None:
            return str(errIndication)
        for name, val in vals:
            return str( int(val.prettyPrint()) / 10 ) 
    

    def set_acs_user_reconf(self,serial):
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )
        print(dec_serial)
        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.16.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),rfc1902.Unsigned32(1) ),
                                )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('acs reconf ',errorIndication)
            return False
        elif errorStatus:
            print('acs reconf ',errorStatus)
            return False
        else:
            print('yep')
            return True
        return True

    def set_acs_user_profile(self,serial,ont_model):
        print(ont_model)
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.3.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),pysnmp.OctetString(ont_model) ),
                                )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('acs profile ',errorIndication)
            return False
        elif errorStatus:
            print('acs profile ',errorStatus)
            return False
        else:
            print('yep')
            return True
        return True

    def set_acs_user_password(self,serial,password):
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.12.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),pysnmp.OctetString(password) ),
                                )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('acs password ',errorIndication)
            return False
        elif errorStatus:
            print('acs paswword ',errorStatus)
            return False
        else:
            print('yep')
            return True
        return True

    def set_acs_user_login(self,serial,login):
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.11.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),pysnmp.OctetString(login) ),
                                )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('acs login ',errorIndication)
            return False
        elif errorStatus:
            print('acs login ',errorStatus)
            return False
        else:
            print('yep')
            return True
        return True
    
    def set_acs_user_personal(self,serial,personal):
        st= ''
        r = []
        serial = serial.replace('ELTX','454C5458')
        for i,num in enumerate(serial):
             st +=num
             if i%2 != 0:
                 r.append(st)
                 st = ''
        
        dec_serial = '.'.join( list(map(lambda x: str(int(x,16)),r)) )

        OID = f'1.3.6.1.4.1.35265.1.22.3.15.1.2.8.{dec_serial}'

        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port) ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),pysnmp.OctetString(personal) ),
                                )
        )
        
        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('acs user ',errorIndication)
            return False
        elif errorStatus:
            print('acs user ',errorStatus)

            return False
        else:
            print('yep')
            return True
        return True
    
    def set_save(self):
        OID = '1.3.6.1.4.1.35265.1.22.1.50.0'
        iterator = next(pysnmp.setCmd(
                                pysnmp.SnmpEngine(),
                                pysnmp.CommunityData(self.community),
                                pysnmp.UdpTransportTarget( (self.ip, self.port),timeout=15.0 ),
                                pysnmp.ContextData(),
                                pysnmp.ObjectType(pysnmp.ObjectIdentity(OID),rfc1902.Unsigned32(1) ),
                                )
        )

        errorIndication, errorStatus, errorIndex, vals = iterator
        if errorIndication:
            print('OLT save ',errorIndication)
            return False
        elif errorStatus:
            print('OLT save ',errorStatus)
            return False
        else:
            print('saved')
            return True
        return True