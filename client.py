import socket
import argparse
import time
import binascii

HOST = ''
PORT = 10005

def new_parser():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(help='commands')
      
    # A createblockchain command
    typeSign_parser = sub_parser.add_parser(
        'gettypesign', help='Apply for a permission signature of new coin NEWCOINTYPE')
    typeSign_parser.add_argument(
        '--cointype', type=str, dest='new_coin_type', help='NEWCOINTYPE')
    return parser


def getTypeSign(coin_type, s):
    s.send(b"gettypesign")
    s.send(coin_type.encode('UTF-8'))
    data = s.recv(1024)
    print("Type Signature : ",binascii.hexlify(data))




if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connected to " + HOST + str(PORT))
    parser = new_parser()
    args = parser.parse_args()

    if hasattr(args, 'new_coin_type'):
        getTypeSign(args.new_coin_type, s)
    

    s.close()


# command
"""
python cli.py createblockchain --address Ivan --subsidy 200 --cointype BAR
python cli.py getbalance --address Ivan
python cli.py send --from Ivan --to Danny --cointype BAR --amount 20
python cli.py addcoin --subsidy 2000 --cointype JIMBEAN --address Pierre
python cli.py send --from Pierre --to Danny --cointype JIMBEAN --amount 66
python cli.py getbalance --address Pierre
python cli.py addcoin --subsidy 900 --cointype KIRIN --address Cynthia
python cli.py print
python client.py gettypesign --cointype BAR
"""
	