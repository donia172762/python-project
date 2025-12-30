# task2_pattern_exposure.py
# Show why ECB leaks patterns while CBC hides them using repeated 16-byte blocks.

from collections import Counter
from task2_aes import (
    key_expansion, aes_encrypt_block,
    hex_to_bytes, bytes_to_hex
)

BLOCK = 16

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def ecb_encrypt_exact(key: bytes, pt: bytes) -> bytes:
    """AES-128 ECB, no padding. Length must be multiple of 16."""
    assert len(pt) % BLOCK == 0
    rk = key_expansion(key)
    out = bytearray()
    for i in range(0, len(pt), BLOCK):
        out += aes_encrypt_block(pt[i:i+BLOCK], rk)
    return bytes(out)

def cbc_encrypt_exact(key: bytes, iv: bytes, pt: bytes) -> bytes:
    """AES-128 CBC, no padding. Length must be multiple of 16."""
    assert len(pt) % BLOCK == 0
    rk = key_expansion(key)
    out = bytearray()
    prev = iv
    for i in range(0, len(pt), BLOCK):
        blk = xor_bytes(pt[i:i+BLOCK], prev)
        c = aes_encrypt_block(blk, rk)
        out += c
        prev = c
    return bytes(out)

def split_blocks(b: bytes):
    return [b[i:i+BLOCK] for i in range(0, len(b), BLOCK)]

def summarize(ct: bytes, label: str, show=4):
    blocks = split_blocks(ct)
    unique = len(set(blocks))
    counts = Counter(blocks)
    print(f"{label}:")
    print(f"- total blocks         : {len(blocks)}")
    print(f"- unique blocks        : {unique}")
    print(f"- most common block rep: {max(counts.values())}")
    print(f"- first {show} blocks (hex):")
    for i, bl in enumerate(blocks[:show]):
        print(f"  B{i:02d} = {bl.hex()}")
    print()

def main():
    # Fixed key/IV so you can copy results into the report
    key_hex = "00112233445566778899aabbccddeeff"
    iv_hex  = "000102030405060708090a0b0c0d0e0f"
    key = hex_to_bytes(key_hex)
    iv  = hex_to_bytes(iv_hex)

    # 16-byte block to repeat (same block over and over)
    base_blk = hex_to_bytes("00112233445566778899aabbccddeeff")
    num_blocks = 32  # any N ≥ 8 works; 32 is clear in the summary
    pt = base_blk * num_blocks

    # Encrypt with ECB and CBC (no padding; exact multiples of 16)
    ct_ecb = ecb_encrypt_exact(key, pt)
    ct_cbc = cbc_encrypt_exact(key, iv, pt)

    print("=== Repeated-Block Pattern Demo (no images) ===")
    print(f"Key = {key_hex}")
    print(f"IV  = {iv_hex}\n")
    summarize(ct_ecb, "ECB ciphertext")
    summarize(ct_cbc, "CBC ciphertext")

if __name__ == "__main__":
    main()
