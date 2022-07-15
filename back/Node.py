from .models import Node, Node_map, Edge, Position
from .Switch import Switch
from .Ports import SWITCHPORT

def get_all_data_on_map(node_map):
    Map = Node_map.objects.filter(name=node_map).first()
    data = []
    for node in Map.nodes.all():
        node_data = {}
        node_data['ip'] = node.ip
        node_data['name'] = node.name
        node_data['model'] = node.model
        node_data['directionText'] = node.directionText
        node_data['connections'] = []

        for edge in Map.edges.filter(on=node):
            node_data['connections'].append({
                'on_port': edge.on_port,
                'to_port': edge.to_port,
                'to_ip' : edge.to.ip
            })
        
        pos_data = Map.positions.filter(node=node).first()
        if pos_data:
            node_data['position'] = {
                'x': pos_data.x,
                'y': pos_data.y
            }
        else:
            node_data['position'] = {
                'x' : 0,
                'y' : 0
            }

        if node_data['model'] == 'MES3324':
            node_data['ports'] = SWITCHPORT.get_ports_mes3324()
        elif node_data['model'] == 'QSW2850':
            node_data['ports'] = SWITCHPORT.get_ports_qsw2850()

        data.append(node_data)
    
    return data

def save_map(data):
    Map = Node_map.objects.filter(name=data['node_map']).first()
    node_data = data['data']
    for node in node_data:
        n = Node.objects.filter(ip=node['ip'])
        if n:
            n = n[0]
        else:
            print('Create Node ', node['ip']) 
            n = Node(ip=node['ip'],name=node['name'],model=node['model'])
            n.save()

        if not Map.nodes.filter(pk=n.pk).exists():
            print('Add to Map ', node['ip'])
            Map.nodes.add(n)
            Map.save()

        pos_data = Map.positions.filter(node=n).first()
        if pos_data:
            pos_data.x = node['position']['x']
            pos_data.y = node['position']['y']
            pos_data.save()
        
        exists_edges = Map.edges.filter(on=n)
        new_edges = node['connections']
        new_edges_ips = [ n['to_ip'] for n in new_edges]
        for ex in exists_edges:
            if ex.to.ip not in new_edges_ips:
                print("EDGE NOT EXISTS")
        '''
        for nedges in node.connections:
            t = Node.objects.filter(ip=nedges['to_ip'])
            if t:
                t = t[0]
                exists_edge = Map.edges.filter(on=n,to=t)
                if exists_edge:
                    exists_edge = exists_edge[0]
                    if not all(exists_edge.on_port == nedges['on_port'],
                               exists_edge.to_port == nedges['to_port']):
                               
                               exists_edge.on_port = nedges['on_port']
                               exists_edge.to_port = nedges['to_port']
                
            else:
                
                #exists_edge = Map.edges.filter(on=n,)    
        '''

def get_ports_on_vlan(data):
    ip = data['ip']
    vlan = data['vlan']
    print(ip,vlan)
    sw = Switch(ip,community='private_set')
    return sw.get_ports_on_vlan(vlan)

def add_access_vlan(data):
    ip = data['ip']
    vlan = data['vlan']
    port = data['port']
    sw = Switch(ip,community='private_set')
    return sw.set_access_vlan_on_port(port,vlan)

def add_trunk_vlans(data):
    ip = data['ip']
    vlans = data['vlan'].split(',')
    port = data['port']
    print(vlans,port)
    sw = Switch(ip,community='private_set')
    return sw.set_trunk_vlans_on_port(port,vlans)
