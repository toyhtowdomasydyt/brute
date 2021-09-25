from multiprocessing import Pool, cpu_count
from itertools import product, islice
from random import SystemRandom
from hashlib import sha224
from Loader import Loader

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


def distribute_data(cores, variants):
    return [
        {
            "start": math.ceil(variants / cores * i),
            "stop": math.ceil(variants / cores) * (i + 1)
        }
        for i in range(cores)
    ]


def distribute_brute(org_hash, passwords, breakpoints):
    cores = cpu_count()

    with Pool(cores) as pool:
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
                    password = jobs[i].get()
                    pool.terminate()
                    stop = True
                    break

        pool.join()
        return password


def main():
    alphabet = string.ascii_letters
    strength = 5
    cores = cpu_count()

    print(f"Cores in your PC: {cores}\n")

    # Generate password and its hash (needs SystemRandom method from random module)
    # org_pass = ''.join(SystemRandom().choice(string.ascii_letters) for _ in range(strength))
    # org_hash = get_hash(org_pass, sha224)

    org_hash = '090ec244dc136b692f252ea2409b9c499794f2db7b37da089dcc9b8a'

    with Loader("Cracking..."):
        passwords = product(alphabet, repeat=strength)

        variants = get_variants(strength, len(alphabet))
        breakpoints = distribute_data(cores, variants)

        password = distribute_brute(org_hash, passwords, breakpoints)

    print(f"\nThe password: {password}")


if __name__ == '__main__':
    start = time.time()

    main()

    print(f"--- {round((time.time() - start), 5)} seconds ---")
