from blockchain.backend.core.elleptic_curve.elleptic_curve import Sha256Point
import secrets


class Account:
    def create_keys(self):
        """Secp256k1 Curve Generator Points"""
        g_x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        g_y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

        g = Sha256Point(g_x, g_y)

        private_key = secrets.randbits(256)
        print("PRIVATE KEY IS: ", private_key)


if __name__ == "__main__":
    account = Account()
    account.create_keys()