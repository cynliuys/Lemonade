#finished
import argparse

from blockchain import Blockchain
from transaction import UTXOTx, CoinbaseTx
from pow import Pow

def new_parser():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(help='commands')
    # A print command
    print_parser = sub_parser.add_parser(
        'print', help='Print all the blocks of the blockchain')
    print_parser.add_argument('--print', dest='print', action='store_true')
    # A getbalance command
    balance_parser = sub_parser.add_parser(
        'getbalance', help='Get balance of ADDRESS')
    balance_parser.add_argument(
        '--address', type=str, dest='balance_address', help='ADDRESS of balance')
    # A printblock command
    printblock_parser = sub_parser.add_parser(
        'printblock', help='Print block whose height is HEIGHT')
    printblock_parser.add_argument(
        '--height', type=int, dest='block_height', help='HEIGHT of block')    
    # A createblockchain command
    bc_parser = sub_parser.add_parser(
        'createblockchain', help='Create a blockchain and send genesis block reward SUBSIDY COINTYPE coins to ADDRESS')
    bc_parser.add_argument(
        '--address', type=str, dest='blockchain_address', help='ADDRESS')
    bc_parser.add_argument(
        '--subsidy', type=int, dest='subsidy', help='SUBSIDY')
    bc_parser.add_argument(
        '--cointype', type=str, dest='coin_type', help='COINTYPE')
    # A createcoin command
    ac_parser = sub_parser.add_parser(
        'addcoin', help='Add a new coin COINTYPE and send SUBSIDY COINTYPE coins to ADDRESS')
    ac_parser.add_argument(
        '--subsidy', type=int, dest='subsidy', help='SUBSIDY')
    ac_parser.add_argument(
        '--cointype', type=str, dest='coin_type', help='COINTYPE')
    ac_parser.add_argument(
        '--address', type=str, dest='add_coin_address', help='ADDRESS')
    # A send command
    send_parser = sub_parser.add_parser(
        'send', help='Send AMOUNT of COINTYPE coins from FROM address to TO')
    send_parser.add_argument(
        '--from', type=str, dest='send_from', help='FROM')
    send_parser.add_argument(
        '--to', type=str, dest='send_to', help='TO')
    send_parser.add_argument(
        '--cointype', type=str, dest='coin_type', help='COINTYPE')
    send_parser.add_argument(
        '--amount', type=int, dest='send_amount', help='AMOUNT')

    return parser


def get_balance(address):
    bc = Blockchain()

    balance = dict()
    UTXOs = bc.find_utxo(address)

    for out in UTXOs:
        if out.cointype not in balance.keys():
            balance[out.cointype] = 0 
        balance[out.cointype] += out.value

    print('Balance of {0}:'.format(address))
    print('----------------------')
    for c,b in balance.items():
        print('{0}: {1}'.format(c, b))


def create_blockchain(subsidy, cointype, address):
    assert subsidy is not None
    assert cointype is not None
    assert address is not None
    Blockchain(subsidy, cointype, address)
    print('Successfully created blockchain!')


def add_coin(subsidy, cointype, address):
    bc = Blockchain()

    cb_tx = CoinbaseTx(address, subsidy, cointype).set_id()
    bc.MineBlock([cb_tx])
    print('Successfully added new coin: {} !'.format(cointype))

    
def print_chain(height=-1):
    bc = Blockchain()

    for block in bc.blocks:
        if (height == -1) or (height == block.height):
            print("Prev. hash: {0}".format(block.prev_block_hash))
            print("Hash: {0}".format(block.hash))
            pow = Pow(block)
            print("PoW: {0}".format(pow.validate()))
            print("Height: {0}\n".format(block.height))


def send(from_addr, to_addr, cointype, amount):
    bc = Blockchain()

    tx = UTXOTx(from_addr, to_addr, amount, cointype, bc).set_id()
    bc.MineBlock([tx])
    print('Success!')


if __name__ == '__main__':
    parser = new_parser()
    args = parser.parse_args()

    if hasattr(args, 'print'):
        print_chain()
    
    if hasattr(args, 'block_height'):
        print_chain(args.block_height)

    if hasattr(args, 'balance_address'):
        get_balance(args.balance_address)

    if hasattr(args, 'blockchain_address') and \
            hasattr(args, 'coin_type') and \
            hasattr(args, 'subsidy'):
        create_blockchain(args.subsidy, args.coin_type, args.blockchain_address)
    
    if hasattr(args, 'add_coin_address'):
        add_coin(args.subsidy, args.coin_type, args.add_coin_address)

    if hasattr(args, 'send_from') and \
            hasattr(args, 'send_to') and \
            hasattr(args, 'coin_type') and \
            hasattr(args, 'send_amount'):
        send(args.send_from, args.send_to, args.coin_type, args.send_amount)

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
"""