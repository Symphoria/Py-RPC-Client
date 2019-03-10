from rpc import rpc_call
if rpc_call('is_even', 4):
    print('It is even')
else:
    print('Oh! Its odd')
