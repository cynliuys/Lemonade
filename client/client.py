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
    '''
    print(typesig)
    print(binascii.hexlify(typesig))
    print(codecs.decode(binascii.hexlify(typesig), 'hex_codec'))
    print(binascii.b2a_qp(codecs.decode(binascii.hexlify(typesig), 'hex_codec')))
    print("---------------------------------------")
    typesig = binascii.b2a_qp(codecs.decode(binascii.hexlify(typesig), 'hex_codec'))

    print(typesig)
    print(binascii.a2b_qp(typesig))
    print(codecs.encode(binascii.a2b_qp(typesig), 'hex_codec'))
    print(binascii.a2b_hex(codecs.encode(binascii.a2b_qp(typesig), 'hex_codec')))

    # print(type(codecs.decode(binascii.hexlify(typesig), 'hex_codec')))
    data = str(subsidy) + ' ' + cointype + ' ' + name + ' ' + typesig + ' (addcoin)'
    s.send(b'New request')
    s.send(data.encode('utf-8'))
    '''
    s.send(b'New request')
    s.send(data)


def sendCoin(s, from_name, to_name, cointype ,amount ,sig):
    s.send(b'New request')

    data = from_name.encode('utf-8') + b'   ' + to_name.encode('utf-8') + b'   ' + \
           cointype.encode('utf-8') + b'   ' + str(amount).encode('utf-8') + b'   ' +\
           sig + b'   ' + b'(send)'
    s.send(data)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))


    print("Step1 : createType")
    sign = createType(s, 'QQ')
    print(binascii.hexlify(sign))

    print("Step2 : addWallet")
    privateKey1, addr1 = addWallet(s, 'Cynthia')
    print(privateKey1)
    print(addr1)
    privateKey2, addr2 = addWallet(s, 'Pierre')
    print(privateKey2)
    print(addr2)

    print("Step3 : addCoin")
    addCoin(s, 50, 'QQ', 'Cynthia', sign)
    
    time.sleep(2)

    print("Step4 : sendCoin")
    sk = ecdsa.SigningKey.from_string(privateKey1, curve=ecdsa.SECP256k1)
    sig = sk.sign('yes'.encode('UTF-8'))
    sendCoin(s, 'Cynthia', 'Pierre', 'QQ' ,10 ,sig)





    s.close()


