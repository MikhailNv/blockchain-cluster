from script import Script
from utils import (
    int_to_little_endian,
    little_endian_to_int,
    bytes_needed,
    decode_base58,
    encode_variant,
    hash256
)


ZERO_HASH = b'\0' * 32
REWARD = 50
PRIVATE_KEY = "49741362227082407330740833331123012399690311433435024477384729336307231521955"
MINER_ADDRESS = "1NEjbPTvYZqACL6snczJ2gnt4vMRPfhiGC"

class CoinbaseTx:
    def __init__(self, block_height):
        self.block_height_little_endian = int_to_little_endian(block_height, bytes_needed(block_height))

    def coinbase_transaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xffffffff

        tx_ins = []
        tx_ins.append(TxIn(prev_tx, prev_index))
        tx_ins[0].script_sig.cmds.append(self.block_height_little_endian)

        tx_outs = []
        target_amount = REWARD * 100000000
        target_160 = decode_base58(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_160)
        tx_outs.append(TxOut(amount=target_amount, script_pubkey=target_script))

        coinbase_tx = Tx(1, tx_ins, tx_outs, 0)

        return coinbase_tx

class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.tx_id = self.id()

    def id(self):
        return self.hash().hex()

    def hash(self):
        return hash256(self.serialize())[::-1]

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += encode_variant(len(self.tx_ins))

        for tx_in in self.tx_ins:
            result += tx_in.serialize()

        result += encode_variant(len(self.tx_outs))

        for tx_out in self.tx_outs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.locktime, 4)

        return result

    def is_coinbase(self):
        if len(self.tx_ins) != 1:
            return False

        first_input = self.tx_ins[0]

        if first_input.prev_tx != b'\x00' * 32:
            return False

        if first_input.prev_index != 0xffffffff:
            return False

        return True
    def to_dict(self):
        if self.is_coinbase():
            self.tx_ins[0].prev_tx = self.tx_ins[0].prev_tx.hex()
            self.tx_ins[0].script_sig.cmds[0] = little_endian_to_int(self.tx_ins[0].script_sig.cmds[0])
            self.tx_ins[0].script_sig = self.tx_ins[0].script_sig.__dict__

        self.tx_ins[0] = self.tx_ins[0].__dict__

        self.tx_outs[0].script_pubkey.cmds[2] = self.tx_outs[0].script_pubkey.cmds[2].hex()
        self.tx_outs[0].script_pubkey = self.tx_outs[0].script_pubkey.__dict__
        self.tx_outs[0] = self.tx_outs[0].__dict__

        return self.__dict__


class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index

        self.script_sig = script_sig if script_sig else Script()
        self.sequence = sequence

    def serialize(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result


class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result
