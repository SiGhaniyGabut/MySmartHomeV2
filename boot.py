# This is script that run when device boot up or wake from sleep.
import machine, esp, gc, json
from wifi_connect import WiFiConnect
from main.updater import Updater

with open('config.json', 'r') as f: configurations = json.loads(f.read())
f.close()

# Connect to WiFi
WiFiConnect().start(**configurations['wifi'])

has_updated = Updater(configurations['github_repo']).install_update_if_available()

if has_updated: machine.reset()
else:
    del(has_updated)
    del(configurations)
    gc.collect()

esp.osdebug(None)
gc.collect()