import socket
HOST = ''

if __name__ == '__main__':
	
	socketNum = input("How many SOCKETs this server should creat? ")
	PORT = []
	s = []
	# connect to other server
	for i in range(3-int(socketNum)):
		PORT.append(input("Connect port " + str(i+1) + ": "))
		s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
		s[i].connect((HOST, int(PORT[i])))
		print("Connected to " + HOST + PORT[i])

	# creat new socket
	for i in range(3-int(socketNum), 3):
		PORT.append(input("New socket " + str(i+1) + ": "))
		s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
		s[i].bind((HOST, int(PORT[i])))
