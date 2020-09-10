import functions
import generateIp
import time
import multiprocessing
from functools import partial

macAdresses = generateIp.getMacAdresses()
networkAdress = generateIp.generateIP()

isConnectedwithWifi = True

functions.rerunscanNetwork()(networkAdress)

# functions.searchIpWithMac(macAdresses)
#
# while True:
#     functions.scanNetwork()
#     functions.checkIfIpStillOnline()
#     time.sleep(30)
