import os
from decouple import config
import re

ipAddressRegex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")

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

def getNetworkAddres():
    if config("isConnectedWithWifi") == True:
        ips = os.popen("ip addr show wlan0")
    else:
        ips = os.popen("ip addr show eth0")
    for ip in ips:
        find = re.findall(ipAddressRegex,ip)
        if len(find) > 1:
            return(find[0])

def generateIP():
    print(getNetworkAddres())
    return generateDefaultIP(getNetworkAddres())

def getMacAdresses():
    macAddresses = config("macAddresses")
    return macAddresses.split(",")