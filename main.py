import json
from main.entrypoint import EntryPoint

with open('config.json', 'r') as f: configurations = json.loads(f.read())
f.close()

EntryPoint(configurations).run()