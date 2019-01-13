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
    (3)Return the balance of from_name and to_name

5.Get balance 
    (1)Send 'get balance name'
    (2)Return the balance of the name 

'''
import socket
import time
import codecs
import binascii
import ecdsa

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
    privateKey = s.recv(2048)
    address = s.recv(2048).decode('utf-8')
    return privateKey, address


def addCoin(s, subsidy, cointype, name, typesig):
    data = str(subsidy).encode('utf-8') + b'   ' + cointype.encode('utf-8') + b'   ' + \
                name.encode('utf-8') + b'   ' + typesig + b'   (addcoin)'
    s.send(b'New request')
    time.sleep(1)
    s.send(data)
    result = s.recv(2048).decode('utf-8')
    return result



def sendCoin(s, from_name, to_name, cointype ,amount ,sig):
    s.send(b'New request')
    data = from_name.encode('utf-8') + b'   ' + to_name.encode('utf-8') + b'   ' + \
           cointype.encode('utf-8') + b'   ' + str(amount).encode('utf-8') + b'   ' +\
           sig + b'   ' + b'(send)'
    s.send(data)
    balance = s.recv(2048)
    return balance.decode('utf-8')


def getBalance(s, name):
    data = 'get balance ' + name
    s.send(data.encode('utf-8'))
    balance = s.recv(2048)
    return balance


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))


    print("Step1 : createType QQ and RR")
    sign1 = createType(s, 'QQ')
    sign2 = createType(s, 'RR')

    time.sleep(1)

    print("Step2 : addWallet")
    privateKey1, addr1 = addWallet(s, 'Cynthia')
    print('\t-Cynthia is finished !')
    privateKey2, addr2 = addWallet(s, 'Pierre')
    print('\t-Pierre is finished !')

    time.sleep(1)

    print("Step3 : addCoin")
    result = addCoin(s, 50, 'QQ', 'Cynthia', sign1)
    print(result)
    time.sleep(2)
    
    result = addCoin(s, 50, 'RR', 'Pierre', sign2)
    print(result)
    
    
    time.sleep(1)

    print("Step4 : sendCoin")
    sk = ecdsa.SigningKey.from_string(privateKey1, curve=ecdsa.SECP256k1)
    sig = sk.sign('yes'.encode('UTF-8'))
    balance = sendCoin(s, 'Cynthia', 'Pierre', 'QQ' ,10 ,sig)
    print('Cynthia balance :\n'+ balance)

    time.sleep(1)
    
    sk = ecdsa.SigningKey.from_string(privateKey2, curve=ecdsa.SECP256k1)
    sig = sk.sign('yes'.encode('UTF-8'))
    balance = sendCoin(s, 'Pierre', 'Cynthia', 'RR' ,20 ,sig)
    print('Pierre balance :\n'+ balance)
    


    time.sleep(1)

    print("step5: ask for balance")
    A_balance = getBalance(s, 'Cynthia')
    B_balance = getBalance(s, 'Pierre')
    print('Cynthia balance :', A_balance.decode('utf-8'))
    print('Pierre balance :\n'+ B_balance.decode('utf-8'))

    s.close()


