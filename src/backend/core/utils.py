import hashlib
from Crypto.Hash import RIPEMD160
from hashlib import sha256
from math import log

from src.backend.core.elleptic_curve import BASE58_ALPHABET


def hash256(string):
    """Two round of sha256"""
    first_iter = hashlib.sha256(string).digest()
    second_iter = hashlib.sha256(first_iter).digest()
    return second_iter


def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()


def bytes_needed(n):
    if n == 0:
        return 1
    return int(log(n, 256)) + 1


def int_to_little_endian(n, length):
    """Takes an integer and return the little-endian sequence of length"""
    return n.to_bytes(length, 'little')


def little_endian_to_int(b):
    return int.from_bytes(b, 'little')


def decode_base58(s):
    num = 0

    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)

    combined = num.to_bytes(25, byteorder='big')
    checksum = combined[-4:]

    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(f"Incorrect address {checksum} {hash256(combined[:-4])[:4]}")
    return combined[1:-4]


def encode_variant(i):
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise ValueError(f"Число {i} типа integer слишком велико")