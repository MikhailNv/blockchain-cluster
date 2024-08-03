from utils import hash256


class BlockHeader:
    def __init__(self, version, previous_block_hash, merkle_root, timestamp, bits):
        self.version = version
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.block_hash = ""

    def mine(self):
        while self.block_hash[0:4] != "0000":
            concatenate_string = (
                    str(self.version) +
                    self.previous_block_hash +
                    self.merkle_root +
                    str(self.timestamp) +
                    self.bits +
                    str(self.nonce)
            ).encode()
            self.block_hash = hash256(concatenate_string).hex()
            self.nonce += 1