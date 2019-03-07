import json


def marshal_boolean(arg):
    if arg:
        return '1'
    else:
        return '0'


def marshal(arg, type):
    if type == 'boolean':
        return marshal_boolean(arg)

    return json.dumps(arg)
