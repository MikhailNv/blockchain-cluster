import hashlib


def hash256(string):
    """Two round of sha256"""
    first_iter = hashlib.sha256(string).digest()
    second_iter = hashlib.sha256(first_iter).digest()
    return second_iter
