import subprocess
import re
import sys
#from pushover import Client
from usbip_detach import detach

# replace with your server ip
servers = ('192.168.1.144', '192.168.1.150')
# replace with your device id
device_id = '10c4:8a2a'

usbip_cmd = '/usr/sbin/usbip'

def attach():
    for server in servers:
        try:
            result = subprocess.run([usbip_cmd, 'list', f'--remote={server}'], capture_output=True, timeout=2)
        except subprocess.TimeoutExpired:
            print(f'list time out. {server} is not available')
            continue

        dev_list = str(result.stdout)
        m = re.findall(r'\\n\s+([\d\.-]+):', dev_list)
        if len(m):
            print(f'device found: {m[0]} on {server}')
            # attach usbip
            result = subprocess.run([usbip_cmd, 'attach', f'--remote={server}', f'--busid={m[0]}'], capture_output=True)
            msg = ''
            if result.returncode == 0:
                msg = f'usbip - device attached. device: {m[0]}, server: {server}'
            else:
                err_msg = result.stderr.decode('utf-8')
                msg = f'usbip - attach device failed. errorcode: {result.returncode}, error: {err_msg}'
            print(msg)
            # send pushover message
            #Client(pushover_usr, api_token=pushover_api).send_message(msg)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        device_id = sys.argv[1]
        print(f'using device_id from argument: {device_id}')
    if len(sys.argv) > 2:
        servers = sys.argv[2].split('|')
        print(f'using servers from argument: {servers}')
    detach()
    attach()