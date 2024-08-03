import sys

from core.elleptic_curve.elleptic_curve import Sha256Point, BASE58_ALPHABET
from core.utils import hash160, hash256
from core.database.database import AccountDB
import secrets


class Account:
    def create_keys(self):
        """Secp256k1 Curve Generator Points"""
        g_x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        g_y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

        g = Sha256Point(g_x, g_y)

        private_key = secrets.randbits(256)
        uncompressed_public_key = private_key * g
        x_point = uncompressed_public_key.x
        y_point = uncompressed_public_key.y

        if y_point.num % 2 == 0:
            compressed_key = b'\x02' + x_point.num.to_bytes(32, "big")
        else:
            compressed_key = b'\x03' + x_point.num.to_bytes(32, "big")

        hsh160 = hash160(compressed_key)
        main_prefix = b'\x00'
        new_address = main_prefix + hsh160

        checksum = hash256(new_address)[:4]
        new_address = new_address + checksum

        count = 0
        for zero in new_address:
            if zero == 0:
                count += 1
            else:
                break
        number = int.from_bytes(new_address, "big")
        prefix = '1' * count

        result = ""
        while number > 0:
            number, mod = divmod(number, 58)
            result = BASE58_ALPHABET[mod] + result

        public_address = prefix + result
        setattr(self, "private_key", private_key)
        setattr(self, "public_address", public_address)
        print("PRIVATE_KEY: ", private_key)
        print("PUBLIC_KEY: ", public_address)


if __name__ == "__main__":
    account = Account()
    account.create_keys()
    AccountDB().write([account.__dict__])