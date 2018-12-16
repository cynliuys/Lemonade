# finished
import sys
import pickle 
import utils
try:
    from logbook import Logger
    Logger = Logger   # Does nothing except it shuts up pyflakes annoying error
except ImportError:
    from logging import Logger
from errors import NotEnoughFundsError
from abc import ABCMeta, abstractclassmethod

"""
1. _script_sig in TxInput
2. script_pubkey in TxOutput (and why is the _ missing)
3. what does the decorator @property do, since I don't see the definition of this decorator
"""

class TxInput(object):
    """ Represents a transaction input
    Args:
        txid (string): Transaction ID.
        vout (int): Transaction output value.
        sig (string): Signature script.
    Attributes:
        _tx_id (bytes): Transaction ID.
        _vout (int): Transaction output value.
        _script_sig (string): Signature script.
    """
    def __init__(self, txid, vout, sig):
        self._tx_id = utils.encode(txid) #txid of former transaction
        self._vout = vout # the index of this TxInput among TxInputs
        self._script_sig = sig

    def __repr__(self):
        return 'TXInput(tx_id={0!r}, vout={1!r}, script_sig={2!r})'.format(self._id, self._vout, self._script_sig)

    def can_unlock_output_with(self, unlocking):
        return self._script_sig == unlocking
        # wtf is _script_sig

    @property
    def tx_id(self):
        return utils.decode(self._tx_id)
    
    @property
    def vout(self):
        return self._vout


class TxOutput(object):
    """ Represents a transaction output
    Args:
        value (int): Transaction output.
        pubkey (string): Script of pubkey. (whose pubkey is this?)
    Attributes:
        value (int): Transaction output.
        script_pubkey (string): Script of pubkey.
    """
    
    subsidy = 10
    # the amount of reward
    # why is the subsidy defined here

    def __init__(self, value, pubkey):
        self._value = value
        self.script_pubkey = pubkey

    def __repr__(self):
        return 'TXOutput(value={0!r}, script_pubkey={1!r})'.format(
            self._value, self.script_pubkey)

    def canbe_unlocked_with(self, unlocking):
        return self.script_pubkey == unlocking

    @property
    def value(self):
        return self._value

class Transaction(object):
    """ Represents a ABC transaction 
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self._id = None
        self._vin = None
        self._vout = None

    @property
    def ID(self):
        return self._id

    @property
    def vin(self):
        return self._vin

    @property
    def vout(self):
        return self._vout

    def set_id(self):
        # sets ID of a transaction
        self._id = utils.sum256(pickle.dumps(self))
        return self

    @abstractclassmethod
    def tx_type(self):
        raise NotImplementedError


class CoinbaseTx(Transaction):
    """ Represents a coinbase transaction 
    Args:
        to (string): address of coinbase.
        data (string): script of signature.
    Attributes:
        _id (tytes): Transaction ID.
        _vin (list): List of transaction input.
        _vout (list): List of transaction output.
    """

    def __init__(self, to, data=None):
        if not data:
            data = 'Reward to {0}'.format(to)

        self._id = None
        self._vin = [TxInput('', -1, data)]
        self._vout = [TxOutput(TxOutput.subsidy, to)]

    def __repr__(self):
        return 'CoinbaseTx(id={0!r}, vin={1!r}, vout={2!r})'.format(
            self._id, self._vin, self._vout)

    def tx_type(self):
        return u'Coinbase'

    # def is_coinbase(self):
    #     # checks whether the transaction is coinbase
    #     return len(self._vin) == 1 and \
    #         len(self._vin[0].tx_id) == 0 and \
    #         self._vin[0].vout == -1




class UTXOTx(Transaction):
    """ Represents a UTXO transaction 
    Args:
        from_addr (string): address of from.
        to_addr (string): address of to.
        amount (int): amount you should to pay.
        bc (blcokchain object): a blockchain.
    Attributes:
        _id (tytes): Transaction ID.
        _vin (list): List of transaction input.
        _vout (list): List of transaction output.
    """
    
    def __init__(self, from_addr, to_addr, amount, bc):
        inputs = []
        outputs = []

        self.log = Logger('UTXOTx')
        acc, valid_outputs = bc.find_spendable_outputs(from_addr, amount)
        if acc < amount:
            self.log.error('Not enough funds')
            sys.exit()
        
        # Build a list of inputs
        for tx_id, outs in valid_outputs.items():
            for out in outs:
                input = TxInput(tx_id, out, from_addr)
                inputs.append(input)
        
        # Build a list of outputs
        outputs.append(TxOutput(amount, to_addr))
        if acc > amount:
            outputs.append(TxOutput(acc-amount, from_addr))
        
        self._id = None
        self._vin = inputs
        self._vout = outputs
    
    def __repr__(self):
        return 'UTXOTx(id={0!r}, vin={1!r}, vout={2!r})'.format(
            self._id, self._vin, self._vout)

    def tx_type(self):
        return u'UTXO'