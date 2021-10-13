import subprocess
import re
import sys
#from pushover import Client
# replace with your device id
device_id = '10c4:8a2a'
usbip_cmd = '/usr/sbin/usbip'

if len(sys.argv) > 1:
    device_id = sys.argv[1]
    print(f'using device_id from argument: {device_id}')

def detach():
    result = subprocess.run([usbip_cmd, 'port'], capture_output=True)
    m = re.findall(r'Port\s+(\d+):', result.stdout.decode('utf-8'))
    for port in m:
        result = subprocess.run([usbip_cmd, 'detach', f'--port={port}'], capture_output=True)
        msg = ''
        if result.returncode == 0:
            msg = f'usbip - port {port} detached'
        else:
            msg = f'usbip - Error when detaching port. code: {result.returncode}. {result.stderr}'
        print(msg)
        #Client(pushover_usr, api_token=pushover_api).send_message(msg)

if __name__ == '__main__':
    detach()