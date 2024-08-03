import json
import os.path
import sys


class BaseDB:
    def __init__(self):
        root_folder = "blockchain-cluster"
        path = os.getcwd()
        main_folder = path[:int(path.find("blockchain-cluster")) + len(root_folder)]

        self.base_path = '/'.join((main_folder, "data"))
        self.file_path = '/'.join((self.base_path, self.file_name))

    def read(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            open(self.file_path, 'w')

        with open(self.file_path, "r") as f:
            raw = f.readline()

        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []
        return data

    def write(self, item):
        data = self.read()
        if data:
            data = data + item
        else:
            data = item

        with open(self.file_path, "w+") as f:
            f.write(json.dumps(data))


class BlockchainDB(BaseDB):
    def __init__(self):
        self.file_name = "blockchain"
        super().__init__()

    def last_block(self):
        data = self.read()

        if data:
            return data[-1]


class AccountDB(BaseDB):
    def __init__(self):
        self.file_name = "account"
        super().__init__()