import functions

isConnectedwithWifi = True
macAdresses = ["98:09:cf:8c:e9:d9", "60:45:cb:86:23:73", "18:35:d1:07:21:10"]
networkAdress = functions.generateDefaultIP(functions.getNetworkAddres(isConnectedwithWifi))

print(networkAdress)


scanNetwork()
searchIpWithMac()
checkIfIpStillOnline()

# functions.scanNetwork(networkAdress)


functions.searchIpWithMac(macAdresses)
functions.checkIfIpStillOnline()
