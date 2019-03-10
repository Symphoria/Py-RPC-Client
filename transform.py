import ast
import astor
import requests
import json


class FunctionTransformer(ast.NodeTransformer):
    def __init__(self, remote_procedures):
        self.remote_procedures = remote_procedures

    def visit_Call(self, node):
        node_id = node.func.id

        if node_id in self.remote_procedures:
            new_args = node.args[:]
            new_args.insert(0, ast.Str(s=node_id))

            new_node = ast.Call(
                func=ast.Name(id='rpc_call', ctx=ast.Load()),
                args=new_args,
                keywords=node.keywords
            )

            return new_node

        node.args = list(map(lambda child: self.visit_Call(child) if isinstance(child, ast.Call) else child, node.args))

        return node


filepath = "test.py"
data = open(filepath).read()

registry_url = "https://rpc-registry-server.herokuapp.com/all-procedures"
print("Getting Remote Procedures...")
response = requests.get(registry_url)

remote_procedures = json.loads(response.content)
# remote_procedures = ['is_even', 'find_count']

tree = ast.parse(data)
transformer = FunctionTransformer(remote_procedures)
tree = transformer.visit(tree)

ast.fix_missing_locations(tree)

with open("out.py", "w") as f:
    f.write(astor.to_source(tree))
