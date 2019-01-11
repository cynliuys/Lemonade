import binascii
import ecdsa
import base58
import os
import sys
import pickle

def encode(str, code='utf-8'):
    return str.encode(code)


def decode(bytes, code='utf-8'):
    return bytes.decode(code)



def sign(self, priv_key, prev_txs):
    for vin in self.vin:
        if not prev_txs[vin.tx_id].ID:
            self.log.error("Previous transaction is not correct")

    tx_copy = self._trimmed_copy()

    for in_id, vin in enumerate(tx_copy.vin):
        prev_tx = prev_txs[vin.tx_id]
        tx_copy.vin[in_id].signature = None
        tx_copy.vin[in_id].public_key = prev_tx.out[vin.vout].public_key_hash
        tx_copy.ID = tx_copy.hash()
        tx_copy.vin[in_id].public_key = None

        sk = ecdsa.SigningKey.from_string(
            priv_key.hex(), curve=ecdsa.SECP256k1)
        sig = sk.sign(tx_copy.ID)

        self.vin[in_id].signature = sig



def verify(self, prev_txs):
    for vin in self.vin:
        if not prev_txs[vin.tx_id].ID:
            self.log.error("Previous transaction is not correct")

    tx_copy = self._trimmed_copy()

    for in_id, vin in enumerate(tx_copy.vin):
        prev_tx = prev_txs[vin.tx_id]
        tx_copy.vin[in_id].signature = None
        tx_copy.vin[in_id].public_key = prev_tx.out[vin.vout].public_key_hash
        tx_copy.ID = tx_copy.hash()
        tx_copy.vin[in_id].public_key = None

        sig = self.vin[in_id].signature
        vk = ecdsa.VerifyingKey.from_string(
            vin.public_key[2:].decode('hex'), curve=ecdsa.SECP256k1)
        if not vk.verify(sig, tx_copy.ID):
            return False

    return True


def privatekey_to_publickey(key):
    sk = ecdsa.SigningKey.from_string(key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return vk.to_string()


if __name__ == '__main__':
    private_key = os.urandom(32)
    print("Private : " , binascii.hexlify(private_key))

    public_key = privatekey_to_publickey(private_key)
    print("Public : " , public_key)

    kk = b"12345"

    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    sig = sk.sign(kk)


    vk = ecdsa.VerifyingKey.from_string(public_key, curve=ecdsa.SECP256k1)

    if not vk.verify(sig, kk):
        print("NONO")
    else:
        print("YES")

