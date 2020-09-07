from subprocess import Popen, PIPE
from subprocess import Popen, PIPE
import subprocess
import re
import os
from sense_hat import SenseHat

macAdresses = ["98:09:cf:8c:e9:d9","60:45:cb:86:23:73"]
red = (255, 0, 0)
green = (0, 255, 0)

sh = SenseHat()
#Searches in arp cache file for certain macaddresses 
def searchMac():
    pids = os.popen("arp -a")
    for pid in pids:
        macRegex = re.compile(r"(?:[0-9a-fA-F]:?){12}")
        ipAddressRegex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
        deviceName = pid.split()[0]
        mac = re.findall(macRegex,pid)
        ipAddress = re.findall(ipAddressRegex,pid)

        if(len(mac) > 0 and mac[0] in macAdresses):
            print(deviceName, mac, ipAddress)
            sh.clear(green)
       
#scans the network and add found devices to the arp cache file
def scanNetwork():
    with open(os.devnull, "wb") as limbo:
        for n in range(1, 255):
                ip="192.168.1.{0}".format(n)
                result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                        stdout=limbo, stderr=limbo).wait()
                if result:
                        print(ip, "inactive")
                else:
                        print (ip, "active")
#use this if you can't find your mac address
#scanNetwork()
searchMac()

