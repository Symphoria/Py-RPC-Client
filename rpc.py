import sys
import json
import requests

from serialize import marshal
from deserialize import unmarshal


registry_url = "https://rpc-registry-server.herokuapp.com"


def get_signature(proc_name):
    headers = {
        "data": json.dumps({"serviceName": proc_name})
    }
    result = requests.get(registry_url + "/service-provider", headers=headers)

    return json.loads(result.content)


def check_arg(arg, type):
    if type == 'int':
        return isinstance(arg, int)
    elif type == 'string':
        return isinstance(arg, str)
    elif type == 'char':
        return isinstance(arg, str) and len(arg) == 1
    elif type == 'float':
        return isinstance(arg, float)


def rpc_call(proc_name, *args):
    proc_signature = get_signature(proc_name)
    proc_parameters = sorted(proc_signature['parameters'], key=lambda x: x['parameterPosition'])
    payload = {
        "serviceName": proc_name,
        "parameters": []
    }

    with open('config_vars.txt', 'r+') as f:
        request_no = int(f.read())
        payload['request_no'] = request_no
        f.seek(0)
        f.write(str(request_no + 1))
        f.truncate()

    for i, arg in enumerate(args):
        if check_arg(arg, proc_parameters[i]['parameterType']):
            param_body = {
                "parameterPosition": i + 1,
                "parameterValue": marshal(arg, proc_parameters[i]['parameterType'])
            }
            payload["parameters"].append(param_body)
        else:
            sys.exit("ERROR: Value of passed argument does not match type specified in remote procedure signature")

    headers = {
        'Content-Type': 'application/json'
    }
    result = requests.post(proc_signature['serverAddress'], data=json.dumps(payload), headers=headers)
    unmarshalled_result = unmarshal(json.loads(result.content), proc_signature['returnType'])

    return unmarshalled_result
