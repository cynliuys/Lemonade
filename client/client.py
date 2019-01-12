'''
1.Create type
    (1)Send 'Get key pair'
    (2)Send 'CoinType'
    (3)Recv 'Sign'

2.Add wallet
    (1)Send 'Create wallet name'
    (2)Recv 'PrivateKey'
    (3)Recv 'address'

3.Add coin
    (1)Send 'New request'
    (2)Send 'subsidy cointype name typesig (addcoin)'

4.Send coin
    (1)Send 'New request'
    (2)Send 'from_name to_name cointype amount sig (send)'

'''
import socket
import time
import binascii

HOST = ''
port = 10010

def createType(s, coinType):
    s.send(b'Get key pair')
    time.sleep(2)
    s.send(coinType.encode('utf-8'))
    sign = s.recv(2048)
    return sign


def addWallet(s, name):
    data = 'Create wallet ' + name
    s.send(data.encode('utf-8'))
    privateKey = s.recv(2048).decode('utf-8')
    address = s.recv(2048).decode('utf-8')
    return privateKey, address


def addCoin(s, subsidy, cointype, name, typesig):
    s.send(b'New request')
    data = str(subsidy) + ' ' + cointype + ' ' + name + ' ' + typesig + ' (addcoin)'
    s.send(data.encode('utf-8'))


def sendCoin(s, from_name, to_name, cointype ,amount ,sig):
    s.send(b'New request')
    data = from_name + ' ' + to_name + ' ' + cointype + ' ' + str(amount) + ' ' + sig + ' ' + '(send)'
    s.send(data.encode('utf-8'))


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))


    print("Step1 : createType")
    sign = createType(s, 'QQ')
    print(binascii.hexlify(sign))

    print("Step2 : addWallet")
    privateKey, addr = addWallet(s, 'Cynthia')
    print(privateKey)
    print(addr)





    s.close()


