# usbpi.service.py
# requires python 3.9

import subprocess
import re

# replace device_id with your own device
device_id = '10c4:8a2a'

result = subprocess.run(['usbip', 'list', '-l'], capture_output=True)
m = re.findall(r'busid\s+([\d\.-]+)\s+\(([\w:]+)\)', result.stdout.decode('utf-8'))
for device in m:
    if device[1] == device_id:
        print(f'device found: {device[0]}')
        subprocess.run(['usbip', 'bind', f'--busid={device[0]}'])
        subprocess.run(['usbipd', '-d', '-4'])
        break