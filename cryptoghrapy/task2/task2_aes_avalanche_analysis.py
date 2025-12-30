import os, random
from task2_aes import aes_cbc_encrypt

R = 10  # number of repetitions per experiment


def _flip_random_bit(b: bytes) -> bytes:
    data = bytearray(b)
    i = random.randrange(len(data))
    data[i] ^= 1 << random.randrange(8)
    return bytes(data)


def _hamming(a: bytes, b: bytes) -> int:
    return sum(((x ^ y).bit_count()) for x, y in zip(a, b))


def _rand16() -> bytes:
    return os.urandom(16)


def _print_table(title: str, diffs):
    print(title)
    print("Run | Bit Differences (C1 vs C2)")
    print("----+--------------------------")
    for i, d in enumerate(diffs, 1):
        print(f"{i:>3} | {d}")


def main():
    random.seed()
    P1 = _rand16()  # 128-bit
    K1 = _rand16()  # 128-bit
    IV = _rand16()  # 128-bit

    C1 = aes_cbc_encrypt(K1, IV, P1)

    # (a) Plaintext-bit flip
    diffs_a = []
    for _ in range(R):
        P1p = _flip_random_bit(P1)
        C2 = aes_cbc_encrypt(K1, IV, P1p)
        diffs_a.append(_hamming(C1, C2))
    _print_table("Experiment a) Flip one bit in plaintext", diffs_a)

    # (b) Key-bit flip
    diffs_b = []
    for _ in range(R):
        K1p = _flip_random_bit(K1)
        C2 = aes_cbc_encrypt(K1p, IV, P1)
        diffs_b.append(_hamming(C1, C2))
    _print_table("Experiment b) Flip one bit in key", diffs_b)

    print("Comment: For CBC with AES-128, a 1-bit change usually flips about half of the bits in the output on average (strong avalanche).")

if __name__ == "__main__":
    main()