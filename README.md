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
## How It Works
When server (Windows or RPI) starts, it issues a "usbip list -l" command to list all local usb device, it then parse the output and find the busid that matches the device_id, a binding of busid follows and finally the daemon (usbipd) starts and runs an infinite loop to handle the usb packet forwarding.

When client (debian) starts, it looks through each network addresses in the python file and try issuing a "usbip list -r xx.xx.xx.xx" to retrieve the list of remote bind usb devices and extract the device_id and bus_id. If the server is not available the process will be closed after 2s timeout. Once a valid serer is identified, the client issues 'usbip attach -r xx.xx.xx.xx -b x-x.x.x' to attach to the remote server and the attached usb device appears as a local device to the rest of the system

### Use RPI as Server
1. Turn off the Windows computer
2. Plug USB stick into RPI usb port. Reboot RPI
3. Once RPI is booted, turn on Windows computer
4. Script in Windows computer will start VM and script in VM takes care of the server detection and usb attachment work

### Use Windows as Server
1. Turn off the Windows computer
2. Plug USB stick into Windows computer USB port
3. Turn on Windows computer
4. Script in Windows computer will bind and start usbpi daemon, then launch the VM. the rest is the same as the RPI case

Basically if you follow the right sequence you can switch back and forth freely and the home assistant core will never know (or care) where is the usb stick. the stick always appears local to the home assistant. Which also means you can carry your RPI to wherever you want, this is very convenient in the case that you need to pair a z-wave device (e.g., a in wall switch) and have to get the zwave adapter really close to the device.

## Other Notes
Probably the only negative part of this solution is that you have to set host Windows system to TestMode. As mentioned earlier Windows does not have native support to usbip and it also would not allow using a self-signed driver in regular mode. If you would like to go with commercial solution the above mechanism would probably still work but needs modification to work properly.
