from block import Block
from blockheader import BlockHeader
from database.database import BlockchainDB
from tx import CoinbaseTx
import time


ZERO_HASH = "0" * 64
VERSION = 1

class Blockchain:
    def __init__(self):
        pass

    def save_data(self, block):
        blockchain_db = BlockchainDB()
        blockchain_db.write(block)

    def fetch_last_block(self):
        blockchain_db = BlockchainDB()
        return blockchain_db.last_block()

    def genesis_block(self):
        block_height = 0
        previous_block_hash = ZERO_HASH
        self.add_block(block_height, previous_block_hash)

    def add_block(self, block_height, previous_block_hash):
        timestamp = int(time.time())
        coinbase_instance = CoinbaseTx(block_height)
        coinbase_tx = coinbase_instance.coinbase_transaction()
        merkle_root = coinbase_tx.tx_id
        bits = "ffff001f"
        block_header = BlockHeader(VERSION, previous_block_hash, merkle_root, timestamp, bits)
        block_header.mine()
        print(f"блок {block_height} был успешно добыт со значением nonce {block_header}")
        self.save_data([Block(block_height, 1, block_header.__dict__, 1, coinbase_tx.to_dict()).__dict__])

    def main(self):
        last_block = self.fetch_last_block()
        if last_block is None:
            self.genesis_block()
        while True:
            last_block = self.fetch_last_block()
            block_height = last_block["height"] + 1
            previous_block_hash = last_block["block_header"]["block_hash"]
            self.add_block(block_height, previous_block_hash)


if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.main()