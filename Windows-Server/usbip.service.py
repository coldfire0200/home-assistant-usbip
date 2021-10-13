#usb.service.py
import subprocess
import re

# replace device_id with your own device
device_id = '10c4:8a2a'
# replace the path that contains usbip binaries
usbip_dir = 'C:/your_path/usbip/'

result = subprocess.run([usbip_dir + 'usbip', 'list', '-l'], capture_output=True)
m = re.findall(r'busid\s+([\d\.-]+)\s+\(([\w:]+)\)', result.stdout.decode('utf-8'))
for device in m:
    print(f'device found. busid: {device[0]}, device id: {device[1]}')
    if device[1] == device_id:
        print(f'device found: {device[0]}')
        subprocess.run([usbip_dir + 'usbip', 'bind', f'--busid={device[0]}'])
        subprocess.run([usbip_dir + 'usbipd', '-d', '-4'])
        break