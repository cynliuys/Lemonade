import socket
import binascii
import ecdsa
import base58
import os
HOST = ''


class ServerKey():
	def __init__(self):
		self._private_key = os.urandom(32)
		sk = ecdsa.SigningKey.from_string(self._private_key, curve=ecdsa.SECP256k1)
		vk = sk.get_verifying_key()
		self._public_key = vk.to_string()

	def generateTypeSign(self, cointype):
		sk = ecdsa.SigningKey.from_string(self._private_key, curve=ecdsa.SECP256k1)
		sign = sk.sign(cointype.encode('UTF-8'))
		return sign

	def verifyTypeSign(self, cointype, typeSign):
		vk = ecdsa.VerifyingKey.from_string(self._public_key, curve=ecdsa.SECP256k1)
		if not vk.verify(typeSign, cointype.encode('UTF-8')):
			print("Verify failed!!")
		else:
			print("Verify success!!")





if __name__ == '__main__':

	#Initial private and public key
	serverKey = ServerKey()

	#Creat 4 sockets for 3 other server and 1 client
	PORT1 = input("New socket port 1: ")
	s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s1.bind((HOST, int(PORT1)))

	'''
	PORT2 = input("New socket port 2: ")
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s2.bind((HOST, int(PORT2)))

	PORT3 = input("New socket port 3: ")
	s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s3.bind((HOST, int(PORT3)))

	PORT4 = input("New socket port 4: ")
	s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s4.bind((HOST, int(PORT4)))
	'''

	while(True):
		s1.listen(0)
		'''
		s2.listen(0)
		s3.listen(0)
		s4.listen(0)
		print("s1, s2, s3 and s4 is running...")
		'''

		while(True):
			client1, address1 = s1.accept()
			print(str(address1)+" connected")
			try:
				if(client1.recv(1024) == b"gettypesign"):
					cointype = client1.recv(1024).decode('UTF-8') 
					sign = serverKey.generateTypeSign(cointype)
					print(sign)
					client1.send(sign)
					serverKey.verifyTypeSign(cointype, sign)
				
			except:
				print("except")



