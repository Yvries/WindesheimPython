from subprocess import Popen, PIPE
import subprocess
import re
import os
from sense_hat import SenseHat

macAdresses = ["98:09:cf:8c:e9:d9", "60:45:cb:86:23:73"]
networkAdress = "192.168.1.{0}"

addresses = []
red = (255, 0, 0)
green = (0, 255, 0)

sh = SenseHat()
#Searches in arp cache file for certain macaddresses 
def searchIpWithMac():
    pids = os.popen("arp -a")
    for pid in pids:
        macRegex = re.compile(r"(?:[0-9a-fA-F]:?){12}")
        ipAddressRegex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
        deviceName = pid.split()[0]
        mac = re.findall(macRegex,pid)
        ipAddress = re.findall(ipAddressRegex,pid)

        if(len(mac) > 0 and mac[0] in macAdresses):
            #print(deviceName, mac, ipAddress)
            addresses.append(ipAddress[0])
            sh.clear(green)
       
#scans the network and add found devices to the arp cache file
def scanNetwork():
    with open(os.devnull, "wb") as limbo:
        for n in range(1, 255):
                ip=networkAdress.format(n)
                result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                        stdout=limbo, stderr=limbo).wait()
                if result:
                        print(ip, "inactive")
                else:
                        print (ip, "active")

def checkIfIpStillOnline():
    print(addresses)
    for adres in addresses:
        res = subprocess.call(['ping', '-c', '3', adres])
        if res == 0:
            print("ping to", adres, "OK")
            sh.clear(green)
        elif res == 2:
            print("no response from", adres)
            scanNetwork()
        else: 
            print("ping to", adres, "failed!")
            scanNetwork()
            sh.clear(red)

def generateDefaultIP(ip):
    #count lenght of last array
    ipList = ip.split(".")
    ipListLenght = len(ipList) -1 #most of the time the lenght is 3 -- minus one because len doesnt count from 0

    #remove the string from list
    ipList.remove(ipList[ipListLenght])

    #add the "format" string to list
    ipList.append("{0}")

    #join the list with dots
    generatedIp = ".".join(ipList)

    return generatedIp
    
print(generateDefaultIP("192.168.1.543"))

#scanNetwork()
#searchIpWithMac()
#checkIfIpStillOnline()


