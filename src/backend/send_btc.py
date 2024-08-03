from core.utils import decode_base58
from core.script import Script
from core.tx import TxIn, TxOut, Tx
from core.database.database import AccountDB
import time

class SendBTC:
    def __init__(self, from_account, to_account, amount, utxos):
        self.coin = 1000000
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount * self.coin
        self.utxos = utxos

        # Изменяемые данные
        self.is_balance_enough = None
        self.total = 0
        self.fee = 0
        self.change_amount = 0
        self.from_address_script_pubkey = None
        self.from_pubkey_hash = None
        # self.tx_ins = []
        # self.tx_outs = []

    def get_private_key(self):
        all_accounts = AccountDB().read()
        for account in all_accounts:
            if account["public_address"] == self.from_account:
                return account["private_key"]

    def script_public_key(self, public_address):
        h160 = decode_base58(public_address)
        script_pubkey = Script().p2pkh_script(h160)
        return script_pubkey
    def prepare_tx_in(self):
        tx_ins = []

        self.from_address_script_pubkey = self.script_public_key(self.from_account)
        self.from_pubkey_hash = self.from_address_script_pubkey.cmds[2]

        newutxos = {}

        try:
            while len(newutxos) < 1:
                newutxos = dict(self.utxos)
                time.sleep(2)
        except Exception:
            print("Ошибка конвертации Managed Dict в Normal Dict")

        for tx_bytes in newutxos:
            if self.total < self.amount:
                tx_obj = newutxos[tx_bytes]
                for index, tx_out in enumerate(tx_obj.tx_outs):
                    if tx_out.script_public_key.cmds[2] == self.from_pubkey_hash:
                        self.total += tx_out.amount
                        prev_tx = bytes.fromhex(tx_out.id())
                        tx_ins.append(TxIn(prev_tx, index))
                    else:
                        break

        if self.total < self.amount:
            self.is_balance_enough = False

        return tx_ins


    def prepare_tx_out(self):
        tx_outs = []
        to_script_pubkey = self.script_public_key(self.to_account)
        tx_outs.append(TxOut(self.amount, to_script_pubkey))

        self.change_amount = self.total - self.amount - self.fee

        tx_outs.append(TxOut(self.change_amount, self.from_address_script_pubkey))
        return tx_outs

    def sign_tx(self):
        pass

    def prepare_transaction(self):
        tx_ins = self.prepare_tx_in()
        tx_outs = self.prepare_tx_out()
        tx_obj = Tx(1, tx_ins, tx_outs, 0)