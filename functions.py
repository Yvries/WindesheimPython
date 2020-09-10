from subprocess import Popen, PIPE
import subprocess
import re
import os
from sense_hat import SenseHat
import multiprocessing
from functools import partial

macRegex = re.compile(r"(?:[0-9a-fA-F]:?){12}")
ipAddressRegex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")

activeAdresses = []
addresses = []
red = (255, 0, 0)
green = (0, 255, 0)

sh = SenseHat()

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

def scanIp(networkAdress,n):

    with open(os.devnull, "wb") as limbo:
        ip=networkAdress.format(n)
        result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                stdout=limbo, stderr=limbo).wait()
        if result:
            print(ip, "inactive")
        else:
            print (ip, "active")
            return ip

#scans the network and add found devices to the arp cache file
def scanNetwork(networkAdress):
        n = range(1, 255)
        pool = multiprocessing.Pool(50)
        func = partial(scanIp,networkAdress)
        result = pool.map(func, n)
        pool.close()
        pool.join()

        activeAdresses = [i for i in result if i]
        print(activeAdresses)

def checkIfIpStillOnline(networkAdress):
    print(addresses)
    for adres in addresses:
        res = subprocess.call(['ping', '-c', '3', adres])
        if res == 0:
            print("ping to", adres, "OK")
            sh.clear(green)
        elif res == 2:
            print("no response from", adres)
            scanNetwork(networkAdress)
        else:
            print("ping to", adres, "failed!")
            scanNetwork(networkAdress)
            sh.clear(red)
