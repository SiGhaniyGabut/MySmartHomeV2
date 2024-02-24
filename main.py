import json
from main.my_smart_home import MySmartHome

with open('config.json', 'r') as f: configurations = json.loads(f.read())
f.close()

MySmartHome(configurations).run()