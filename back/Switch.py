from .NSnmp import Snmp
from .controller import *

class Switch:
    def __init__(self,ip,community):
        self.snmp = Snmp(ip,community)
        self.model = self._find_model()
        print(self.model)
        if self.model in ['MES3324','MES2324','MES3124']:
            self.controller = MES3324(self.snmp)
        elif self.model in ['QSW-2850-28T-AC']:
            self.controller = QSW2850(self.snmp)
        else:
            self.controller = None
        
        

    def get_vlans_on_port(self,port):
        return self.controller.get_vlans_on_port(port)

    def get_ports_on_vlan(self,vlan):
        return self.controller.get_ports_on_vlan(vlan)
    
    def set_trunk_vlans_on_port(self,port,vlans):
        return self.controller.set_trunk_vlans_on_port(port,vlans)

    def set_access_vlan_on_port(self,port,vlan):
        return self.controller.set_access_vlan_on_port(port,vlan)

    def get_system_description(self):
        return self.snmp.get('1.3.6.1.2.1.1.1.0')
    
    def _find_model(self):
        sysdescr = self.get_system_description()
        if 'MES3324' in sysdescr:
            return 'MES3324'
        elif 'MES3124' in sysdescr:
            return 'MES3124'
        elif 'MES2324' in sysdescr:
            return 'MES2324'
        elif 'MES5324' in sysdescr:
            return 'MES5324'
        elif 'MES5316' in sysdescr:
            return 'MES5316'
        elif 'C2960' in sysdescr:
            return 'Cisco C2960'
        elif 'C2950' in sysdescr:
            return 'Cisco C2950'
        elif 'QSW-2850-10T-AC' in sysdescr:
            return 'QSW-2850-10T-AC'
        elif 'QSW-2850-28T-AC' in sysdescr:
            return 'QSW-2850-28T-AC'
        elif 'QSW-2800-28T-AC' in sysdescr:
            return 'QSW-2800-28T-AC'
        elif 'QSW-4610-28T-AC' in sysdescr:
            return 'QSW-4610-28T-AC'
        elif 'IES1248' in sysdescr:
            return 'zyxel IES1248'
        elif '2148DC' in sysdescr:
            return 'DSLAM 2148DC'
        elif 'QTECH EPON' in sysdescr:
            return 'QTECH QSW-9001'
        elif 'AAM1212-51' in sysdescr:
            return 'Zyxel IES1000'
        elif 'ME360x' in sysdescr:
            return 'ME360x'
        else:
            return sysdescr
    
    def get_model(self):
        return self.model


if __name__ == '__main__':
    sw = Switch('10.3.0.27','private_set')
    print(sw.set_access_vlan_on_port('2','555'))
    