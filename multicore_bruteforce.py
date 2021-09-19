from itertools import product, islice
from hashlib import sha224
from random import SystemRandom

import multiprocessing as mp
import string
import math
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
    cores = mp.cpu_count()

    org_pass = "MwwX"
    org_hash = get_hash(org_pass, sha224)

    print(org_pass)

    passwords = product(alphabet, repeat=strength)

    variants = get_variants(strength, len(alphabet))

    breakpoints = []

    for i in range(cores):
        breakpoints.append(
            {
                "start": math.ceil(variants / cores * i),
                "stop": math.ceil(variants / cores) * (i + 1)
            }
        )

    with mp.Pool(cores) as pool:
        jobs = []
        for i in range(cores):
            jobs.append(
                pool.apply_async(brute, args=(
                    islice(passwords, breakpoints[i]["start"], breakpoints[i]["stop"]),
                    org_hash
                ))
            )

        pool.close()

        stop = False

        while not stop:
            for i in range(cores):
                if jobs[i].ready() and jobs[i].get() is not None:
                    result = jobs[i].get()
                    stop = True
                    pool.terminate()
                    break

        print(result)
        pool.join()


if __name__ == '__main__':
    start = time.time()
    main()
    print("--- %s seconds ---" % (round((time.time() - start), 5)))
