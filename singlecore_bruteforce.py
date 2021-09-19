from itertools import product, islice
from hashlib import sha224
from random import SystemRandom

import multiprocessing as ml
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

    # org_pass = ''.join(SystemRandom().choice(string.ascii_letters) for _ in range(strength))
    org_pass = 'MwwX'
    org_hash = get_hash(org_pass, sha224)

    print(org_pass)

    passwords = product(alphabet, repeat=strength)
    poss_pass = brute(passwords, org_hash)

    print(poss_pass)


if __name__ == '__main__':
    start = time.time()
    main()
    print("--- %s seconds ---" % (round((time.time() - start), 5)))
