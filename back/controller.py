from .Ports import SWITCHPORT

class Functions:
    @staticmethod
    def convert_hex_to_bin(hex_values):
        temp = []
        for i in range(0,len(hex_values)):
          temp.append( bin(int(hex_values[i], 16))[2:].zfill(4) )
     
        return ''.join(temp)

class MES3324:
    def __init__(self,snmp):
        self.snmp = snmp
        self.ports = SWITCHPORT.get_ports_mes3324()

    def get_vlans_on_port(self,in_port):
        port = self.ports[in_port]['index']
        vlans = []
        for i in range(1,5):
            vlans += self.get_dec_vlans( 
                    self.convert_to_hex( 
                        self.snmp.get(f'1.3.6.1.4.1.89.48.68.1.{i}.{port}') 
                    )
                ,1024*(i-1))
        return vlans
    
    def set_trunk_vlans_on_port(self,port,vlans):
        port = self.ports[port]['index']
        vlans_data_table_one = []
        vlans_data_table_two = []
        vlans_data_table_three = []
        vlans_data_table_four = []
        for vlan in vlans:
           int_dec_vlan = int(vlan)
           if int_dec_vlan <= 1024:
             vlans_data_table_one.append(vlan)
           elif int_dec_vlan <= 2048:
             vlans_data_table_two.append(vlan)
           elif int_dec_vlan <= 3072:
             vlans_data_table_three.append(vlan)
           elif int_dec_vlan <= 4095:
             vlans_data_table_four.append(vlan)
        
        many_vlans = [vlans_data_table_one,vlans_data_table_two,vlans_data_table_three,vlans_data_table_four]
        results = []
        for n,vlans_data_table_i in enumerate(many_vlans):
          if vlans_data_table_i:
            created = self.create_vlan(vlans_data_table_i,(n+2),many=True)
            if created:
              exists_vlans_on_port = self.convert_to_hex(self.snmp.get(f'1.3.6.1.4.1.89.48.68.1.{n+1}.{port}'))
              bin_vlans = self.convert_hex_to_bin(exists_vlans_on_port)
              new_bin_vlans = self.add_to_many_place(vlans_data_table_i,bin_vlans,(n+2))
              new_hex_vlans = self.convert_bin_to_hex(new_bin_vlans)
              if new_hex_vlans:
                res = self.snmp.set_hexValue(f'1.3.6.1.4.1.89.48.68.1.{n+1}.{port}',new_hex_vlans)
                results.append( res[0] )
        
        if all(results):
            return True
        else:
            return False

    
    def create_vlan(self,vlan,num,many=False):
        exists_vlans = self.convert_to_hex( self.snmp.get(f'1.3.6.1.4.1.89.48.69.1.{num}.0') )
        
        bin_vlans = self.convert_hex_to_bin(exists_vlans)
       
        new_bin_vlans = ''
        if many:
           new_bin_vlans = self.add_to_many_place(vlan,bin_vlans,num)
        else:
           new_bin_vlans = self.add_to_place(vlan,bin_vlans,num)
        
        new_hex_vlans = self.convert_bin_to_hex(new_bin_vlans)
       
        result = self.snmp.set_hexValue(f'1.3.6.1.4.1.89.48.69.1.{num}.0',new_hex_vlans)
        if result[0]:
            return True
        else:
            print(result[1],vlan)
            return False


    def add_to_many_place(self,vlans,bin_vlans,num):   
      for vlan in vlans:      
         if num == 2:
            bin_vlans = bin_vlans[:(int(vlan)-1)] + '1' + bin_vlans[(int(vlan)-1) + 1:]
         elif num == 3:
            bin_vlans = bin_vlans[:(int(vlan)-1-1024)] + '1' + bin_vlans[(int(vlan)-1-1024) + 1:]
         elif num == 4:
            bin_vlans = bin_vlans[:(int(vlan)-1-2048)] + '1' + bin_vlans[(int(vlan)-1-2048) + 1:]
         elif num == 5:
            bin_vlans = bin_vlans[:(int(vlan)-1-3072)] + '1' + bin_vlans[(int(vlan)-1-3072) + 1:]
        
      return bin_vlans

    def add_to_place(self,vlan,bin_vlans,num):
      if num == 2:
         return bin_vlans[:(int(vlan)-1)] + '1' + bin_vlans[(int(vlan)-1) + 1:]
      elif num == 3:
         return bin_vlans[:(int(vlan)-1-1024)] + '1' + bin_vlans[(int(vlan)-1-1024) + 1:]
      elif num == 4:
         return bin_vlans[:(int(vlan)-1-2048)] + '1' + bin_vlans[(int(vlan)-1-2048) + 1:]
      elif num == 5:
         return bin_vlans[:(int(vlan)-1-3072)] + '1' + bin_vlans[(int(vlan)-1-3072) + 1:]

    def get_ports_on_vlan(self,vlan):
        d = self.snmp.get(f'1.3.6.1.2.1.17.7.1.4.3.1.2.{vlan}')
        return list(
                map(lambda x:
                        [ i for i in self.ports if self.ports[i]['index'] == x][0]
                    ,
                    self.get_dec_vlans( self.convert_to_hex(d),0 )
                )
        )

    def get_dec_vlans(self,hex_vlans,num):
        vlans = []
        it = 0
        for hex_num in hex_vlans:
            if hex_num == '0':
                it += 1
            else:
                n_bin = bin(int(hex_num, 16))[2:].zfill(4)
                for i in range(len(n_bin)):
                    if n_bin[i] == '1':
                        vlans.append( str( 4*it + i+1 + num) )
                it +=1
        return vlans
    
    def convert_to_hex(self,bytes):
        s = ""
        for i in bytes:
            s += ("%0.2X" % ord(i))
        return s
    
    def convert_hex_to_bin(self,hex_values):
        temp = []
        for i in range(0,len(hex_values)):
          temp.append( bin(int(hex_values[i], 16))[2:].zfill(4) )
     
        return ''.join(temp)
    
    def chunks(self,lst, n):
      for i in range(0, len(lst), n):
         yield lst[i:i + n] 

    def convert_bin_to_hex(self,bin_values):
       bin_values = tuple(self.chunks(bin_values,4))
   
       return ''.join( list(map(lambda x: hex(int(x,2))[2:],bin_values)) )
    
    def delete_all_vlans(self,port):
        oids = []
        for i in range(1,8+1):
            oids.append(f'1.3.6.1.4.1.89.48.68.1.{i}.{port}')
        self.snmp.set_hexValue_8oid(oids[0],oids[1],oids[2],oids[3],oids[4],oids[5],oids[6],oids[7],'0'*256)

    def set_access_vlan_on_port(self,port,dec_vlan):
        port = self.ports[port]['index']
        data = {
            'num':0,
            'oid':''
        }
        int_dec_vlan = int(dec_vlan)
        
        if int_dec_vlan <= 1024:
            data['num'] = 0
            data['oid1'] = f'1.3.6.1.4.1.89.48.68.1.1.{port}'
            data['oid2'] = f'1.3.6.1.4.1.89.48.68.1.5.{port}'
        elif int_dec_vlan <= 2048:
            data['num'] = 1
            data['oid1'] = f'1.3.6.1.4.1.89.48.68.1.2.{port}'  
            data['oid2'] = f'1.3.6.1.4.1.89.48.68.1.6.{port}'
        elif int_dec_vlan <= 3072:
            data['num'] = 2
            data['oid1'] = f'1.3.6.1.4.1.89.48.68.1.3.{port}'
            data['oid2'] = f'1.3.6.1.4.1.89.48.68.1.7.{port}'
        elif int_dec_vlan <= 4095:
            data['num'] = 3
            data['oid1'] = f'1.3.6.1.4.1.89.48.68.1.4.{port}'
            data['oid2'] = f'1.3.6.1.4.1.89.48.68.1.8.{port}'

        created = self.create_vlan(dec_vlan,(data['num'] + 2))
        if created:
            self.delete_all_vlans(port)
            fill_nulls_bin = '0'*1024
            bin_vlans = fill_nulls_bin 
            new_bin_vlans = self.add_to_place(dec_vlan,bin_vlans,data['num']+2)
            new_hex_vlans = self.convert_bin_to_hex(new_bin_vlans)
            if new_hex_vlans:
               res = self.snmp.set_hexValue_2oid(data['oid1'],data['oid2'],new_hex_vlans)
               if res[0]:
                   return True
               else:
                   return False

class QSW2850:
    def __init__(self,snmp):
        self.snmp = snmp
        self.ports = SWITCHPORT.get_ports_qsw2850()
    
    def get_ports_on_vlan(self,vlan):
        vlan = vlan.strip()
        hex_ports = self.snmp.get_pysnmp(f'1.3.6.1.2.1.17.7.1.4.3.1.2.{vlan}')[2:]
        bin_ports = Functions.convert_hex_to_bin(hex_ports)
        ports = []
        for i in range(len(bin_ports)):
            if bin_ports[i] == '1':
                ports.append(str(i+1))
        return ports
    
    def get_vlans_on_port(self,port):
        hex_vlans = self.snmp.get_pysnmp(f'1.3.6.1.4.1.27514.100.3.2.1.20.{port}')[2:]
      
        bin_vlans = Functions.convert_hex_to_bin(hex_vlans)
        vlans = []
        for i in range(len(bin_vlans)):
            if bin_vlans[i] == '1':
                vlans.append(str(i))
        return vlans

    def create_vlan(self,vlan):
        res = self.snmp.set_int(f'1.3.6.1.4.1.27514.100.5.1.1.4.{vlan}',1)
        if res[0]:
            return True
        else:
            print(res[1])
            return False

    def set_trunk_vlans_on_port(self,port,vlans):
        created_vlans = []
        for vlan in vlans:
            created_vlans.append( self.create_vlan(vlan) )
        
        if all(created_vlans):
            exists_vlans = self.get_vlans_on_port(port)
            new_vlans = exists_vlans + vlans
            new_vlans = ','.join(new_vlans)
            res = self.snmp.set_string(f'1.3.6.1.4.1.27514.100.3.2.1.20.{port}',new_vlans)
            if res[0]:
                return True
            else:
                print( 'Error adding',res[1] )
                return False
        else:
            print('Error creating vlan')
            return False

    def set_access_vlan_on_port(self,port,vlan):
        if self.create_vlan(vlan):
            res = self.snmp.set_int(f'1.3.6.1.4.1.27514.100.3.2.1.16.{port}',vlan)
            if res[0]:
                return True
            else:
                print( 'Error adding', res[1])
                return False
        else:
            print('Error creating Vlan')
            return False