# This is script that run when device boot up or wake from sleep.
import machine, esp, gc, json
from wifi_connect import WiFiConnect
from main.ota_updater import Github as OTAUpdater

with open('config.json', 'r') as f: configurations = json.loads(f.read())
f.close()

# Connect to WiFi
WiFiConnect(**configurations['wifi']).start()

ota_updater = OTAUpdater(configurations['github_repo'])
has_updated = ota_updater.install_update_if_available()

if has_updated:
    machine.reset()
else:
    del(ota_updater)
    del(configurations)
    gc.collect()

esp.osdebug(None)
gc.collect()