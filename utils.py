import consul
import json

def find_service(service_name):
    consul_client = consul.Consul()

    index, services = consul_client.health.service(service_name, passing=True)

    result = []
    for service in services:
        s = service['Service']
        result.append({
            'id': s['ID'],
            'name': s['Service'],
            'address': s['Address'],
            'port': s['Port']
        })
    
    return result


def register_service(host, port, name):
    consul_client = consul.Consul()
    consul_client.agent.service.register(
        name=name,
        service_id=f'{name}-{int(port)}-1',
        port=int(port),
        address=host,
        tags=['go'],
        check={
            'http': f'http://192.168.0.103:{int(port)}/health',
            'interval': '10s'
        }
    )

def get_dictionary_info_by_key(key):
    consul_client = consul.Consul()
    _, data = consul_client.kv.get(key)
    return json.loads(data['Value'].decode())
