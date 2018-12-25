import socket
HOST = ''

if __name__ == '__main__':

	#Creat 4 sockets for 3 other server and 1 client
	PORT1 = input("New socket port 1: ")
	s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s1.bind((HOST, int(PORT1)))

	PORT2 = input("New socket port 2: ")
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s2.bind((HOST, int(PORT2)))

	PORT3 = input("New socket port 3: ")
	s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s3.bind((HOST, int(PORT3)))

	PORT4 = input("New socket port 4: ")
	s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s4.bind((HOST, int(PORT4)))

	while(True):
		s1.listen(0)
		s2.listen(0)
		s3.listen(0)
		s4.listen(0)
		print("s1, s2, s3 and s4 is running...")

		while(True):
			client1, address1 = s1.accept()
			print(str(address1)+" connected")
			try:
				print("gogo")
			except:
				print("except")

