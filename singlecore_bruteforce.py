from random import SystemRandom
from itertools import product
from hashlib import sha224
from Loader import Loader

import string
import time


def get_variants(strength, alphabet_len):
    return alphabet_len ** strength


def compare_hash(original_hash, poss_pass_hash):
    return poss_pass_hash == original_hash


def get_hash(password, hash_obj):
    return hash_obj(password.encode("utf-8")).hexdigest()


def brute(passwords, org_hash):
    for poss_pass in passwords:
        if compare_hash(org_hash, get_hash("".join(poss_pass), sha224)):
            return "".join(poss_pass)


def main():
    alphabet = string.ascii_letters
    strength = 4

    # Generate password and its hash
    org_pass = ''.join(SystemRandom().choice(string.ascii_letters) for _ in range(strength))
    org_hash = get_hash(org_pass, sha224)

    # org_hash = '090ec244dc136b692f252ea2409b9c499794f2db7b37da089dcc9b8a'

    with Loader("Cracking..."):
        passwords = product(alphabet, repeat=strength)
        poss_pass = brute(passwords, org_hash)

    print(f"\nThe password: {poss_pass}")


if __name__ == '__main__':
    start = time.time()
    main()
    print(f"--- {round((time.time() - start), 5)} seconds ---")
