# Imports
import socket
server_ip = "1.1.1.1"
port = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, port))


s.close()
