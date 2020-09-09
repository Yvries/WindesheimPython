from subprocess import Popen, PIPE
import subprocess
import re
import os
from sense_hat import SenseHat
import multiprocessing

macRegex = re.compile(r"(?:[0-9a-fA-F]:?){12}")
ipAddressRegex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")

addresses = []
red = (255, 0, 0)
green = (0, 255, 0)

sh = SenseHat()

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

def getNetworkAddres(isConnectedwithWifi):
    if isConnectedwithWifi:
        ips = os.popen("ip addr show wlan0")
    else:
        ips = os.popen("ip addr show eth0")
    for ip in ips:
        find = re.findall(ipAddressRegex,ip)
        if len(find) > 1:
            return(find[0])

#Searches in arp cache file for certain macaddresses
def searchIpWithMac(macAdresses):
    pids = os.popen("arp -a")
    for pid in pids:
        deviceName = pid.split()[0]
        mac = re.findall(macRegex,pid)
        ipAddress = re.findall(ipAddressRegex,pid)

        if(len(mac) > 0 and mac[0] in macAdresses):
            print(deviceName, mac, ipAddress)
            addresses.append(ipAddress[0])
            sh.clear(green)

def scanIp(networkAdress,n,limbo):
    ip=networkAdress.format(n)
    result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
            stdout=limbo, stderr=limbo).wait()
    if result:
            print(ip, "inactive")
    else:
            print (ip, "active")

#scans the network and add found devices to the arp cache file
def scanNetwork(networkAdress):
    with open(os.devnull, "wb") as limbo:
        jobs = []
        for n in range(1, 255):
                p = multiprocessing.Process(target=scanIp, args=(networkAdress,n,limbo,))
                jobs.append(p)
                p.start()

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
