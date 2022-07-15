
class SWITCHPORT:
    @staticmethod
    def get_ports_mes3324():
         return {
            '1' : { 'index': '49', 'name': 'gi1/0/1'},
            '2' : { 'index': '50', 'name': 'gi1/0/2'},
            '3' : { 'index': '51', 'name': 'gi1/0/3'},
            '4' : { 'index': '52', 'name': 'gi1/0/4'},
            '5' : { 'index': '53', 'name': 'gi1/0/5'},
            '6' : { 'index': '54', 'name': 'gi1/0/6'},
            '7' : { 'index': '55', 'name': 'gi1/0/7'},
            '8' : { 'index': '56', 'name': 'gi1/0/8'},
            '9' : { 'index': '57', 'name': 'gi1/0/9'},
            '10' : { 'index': '58', 'name': 'gi1/0/10'},
            '11' : { 'index': '59', 'name': 'gi1/0/11'},
            '12' : { 'index': '60', 'name': 'gi1/0/12'},
            '13' : { 'index': '61', 'name': 'gi1/0/13'},
            '14' : { 'index': '62', 'name': 'gi1/0/14'},
            '15' : { 'index': '63', 'name': 'gi1/0/15'},
            '16' : { 'index': '64', 'name': 'gi1/0/16'},
            '17' : { 'index': '65', 'name': 'gi1/0/17'},
            '18' : { 'index': '66', 'name': 'gi1/0/18'},
            '19' : { 'index': '67', 'name': 'gi1/0/19'},
            '20' : { 'index': '68', 'name': 'gi1/0/20'},
            '21' : { 'index': '69', 'name': 'gi1/0/21'},
            '22' : { 'index': '70', 'name': 'gi1/0/22'},
            '23' : { 'index': '71', 'name': 'gi1/0/23'},
            '24' : { 'index': '72', 'name': 'gi1/0/24'},
            '25' : { 'index': '105', 'name': 'te1/0/1'},
            '26' : { 'index': '106', 'name': 'te1/0/2'},
            '27' : { 'index': '107', 'name': 'te1/0/3'},
            '28' : { 'index': '108', 'name': 'te1/0/4'}
        }
    
    @staticmethod
    def get_ports_qsw2850():
        ports = {}
        for i in range(1,29):
            ports[f'{i}'] = {
                'index': str(i),
                'name' : f'eth1/0/{i}'
            }
        
        return ports
    