import os

for i in range(65336):
    os.system('telnet 192.168.1.13'+str(i))  # 'i' is port number
    print("check"+str(i))
