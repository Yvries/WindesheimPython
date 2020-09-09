import functions
import generateIp

macAdresses = generateIp.getMacAdresses()
print(macAdresses)
networkAdress = generateIp.generateIP()

functions.scanNetwork(networkAdress)

functions.searchIpWithMac(macAdresses)

while True:
    functions.checkIfIpStillOnline()
