import sys
import json
import requests

from serialize import marshal
from deserialize import unmarshal


signature = {
    'is_even': {
        'name': 'is_even',
        'parameters': [{ 'position': 1, 'type': 'int' }],
        'server': "http://127.0.0.1:5000/remote-call",
        'returnType': 'boolean'
    },
    'find_count': {
        'name': 'find_count',
        'parameters': [{'position': 1, 'type': 'string'}, {'position': 2, 'type': 'char'}],
        'server': "http://127.0.0.1:5000/remote-call",
        'returnType': 'int'
    }
}


def check_arg(arg, type):
    if type == 'int':
        return isinstance(arg, int)
    elif type == 'string':
        return isinstance(arg, str)
    elif type == 'char':
        return isinstance(arg, str) and len(arg) == 1


def rpc_call(proc_name, *args):
    proc_signature = signature[proc_name]
    proc_parameters = sorted(proc_signature['parameters'], key=lambda x: x['position'])
    payload = {
        "proc_name": proc_name,
        "args": []
    }

    for i, arg in enumerate(args):
        if check_arg(arg, proc_parameters[i]['type']):
            payload["args"].append(marshal(arg, proc_parameters[i]['type']))
        else:
            sys.exit("ERROR: Value of passed argument does not match type specified in remote procedure signature")

    headers = {
        'Content-Type': 'application/json'
    }
    result = requests.post(proc_signature['server'], data=json.dumps(payload), headers=headers)
    unmarshalled_result = unmarshal(json.loads(result.content), proc_signature['returnType'])

    return unmarshalled_result
