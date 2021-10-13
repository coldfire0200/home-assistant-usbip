# home-assistant-usbip
Add usbip support to home assistant running in Windows Hyper-V

## What you will achieve
This tutorial demonstrates how to add usb support (using usbip) to home assistant system running in Windows Hyper-V. USB device (zigbee/zwave combo stick) can be plugged either in the Windows machine (local) or a Raspberry Pi 3B+ (remote). The python script in the Debian (where home assistant runs) scans available network adddresses and automatically attach to the available server.

## Pre-requisite
### Installation of Home Assistant Supervised
Create a new VM in Hyper-V manager. Install Debian 11. Follow the instructions: https://github.com/home-assistant/architecture/blob/master/adr/0014-home-assistant-supervised.md and https://github.com/home-assistant/supervised-installer to complete home assistant installation. After everything done, configure the VM to start manually, and shutdown with the host system.

### Build Windows Usbip Driver and Tools
usbip is natively supported in Linux kernel. however it is not available on Windows. There are several paid software solutions exist (VirtualHere is one of the cheaper one for $50) but in this tutorial we will go with the free solution: https://github.com/cezanne/usbip-win. The instruction is detailed, accurate and easy to follow. By the end you should have all required driver and executables. ***Warning: you should always try to build the driver yourself, instead of downloading from unknown website. Driver is running in kernel space and also has access to network, you really don't want any malicious code in there.*** To run the self-signed driver you need to put Windows in TestMode. If you don't feel comfortable of doing that, go with the commercial software. There is a good tutorial on this: https://dvlup.com/2020/10/23/usb-in-hyper-v/

Ok by now we finished most of the heave-lifting work

## Raspberry Pi Server
1. install usbip
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install usbip
```
2. load the usbip_host module

   copy the /RPI-Server/etc/modules-load.d/usbip.conf to corresponding folder on RPI

3. setup the usbip service

   copy the /RPI-Server/etc/systemd/system/usbip.service to corresponding folder on RPI

   In usbip.service, change the python executable to match your own configuration. python 3.9 is recommended (tested)

   copy the /RPI-Server/home/pi/usbip.service.py to corresponding folder on RPI

   in usbip.service.py, change the device_id to match your own usb device

   do a test run to make sure things work (no error):
```
sudo systemctl enable usbip
```
Then enable the service:
```
sudo systemctl enable usbip
```
## Windows Server
1. copy /Windows-Server/usbip.service.py to a local directory. change the device_id and usbip tools path to match your own configuration
2. Open Task Scheduler and create a task
   - General tab: select "Run only when user is logon" and check "run with highest priviledge"
   - Trigger: at log on of XXX
   - Actions
     - "Start a program", powershell, Start-Process -FilePath 'python' -ArgumentList 'c:/your_path/usbip/usbip.service.py'
     - "Start a program", powershell, Start-VM 'Your_VM_name'
3. Make Windows auto-logon (I prefer registry edit method. should be plenty of tutorial online)

## Home Assistant (Debian) Client 
1. install usbip
2. load vhci-hcd module

   copy /Debian-Client/etc/modules-load.d/vhci-hcd.conf to corresponding folder on Debian

3. setup the usbip service

   copy /Debian-Client/etc/systemd/system/usbip-attach.service to corresponding folder on Debian

   copy /Debian-Client/opt/application/usbip_attach.py and usbip_detach.py to corresponding folder on Debian

   edit the python file, change the device_id to match your own device

   enable the service:
```
sudo systemctl enable usbip-attach
```
## Other Notes
