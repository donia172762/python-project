import os, random
from task2_aes import aes_cbc_encrypt, aes_cbc_decrypt

BLOCK = 16


def _split_blocks(b: bytes, bs=BLOCK):
    return [b[i:i+bs] for i in range(0,len(b),bs)]

def _flip_random_bit(b: bytes) -> bytes:
    ba = bytearray(b)
    idx = random.randrange(len(ba))
    ba[idx] ^= 1 << random.randrange(8)
    return bytes(ba), idx


def analysis_bit_error(num_blocks=4):
    print("(a) Bit Error in Ciphertext")
    key, iv = os.urandom(16), os.urandom(16)
    # Make multi-block plaintext (exact multiple of 16 so pad adds a full block)
    P = os.urandom(num_blocks*BLOCK)
    C = aes_cbc_encrypt(key, iv, P)

    C_err, flipped_idx = _flip_random_bit(C)
    P_dec = aes_cbc_decrypt(key, iv, C_err)

    P_blocks     = _split_blocks(P)
    Pdec_blocks  = _split_blocks(P_dec)

    # Compare block by block (ignore last pad block by aligning to len(P))
    affected = []
    for i in range(len(P_blocks)):
        same = (P_blocks[i] == Pdec_blocks[i])
        if not same:
            affected.append(i)
    print(f"- Flipped bit at ciphertext byte offset: {flipped_idx}")
    print("- Affected plaintext blocks:", affected)
    print("- Observation: In CBC, corrupting C_i makes P_i fully garbled and flips one bit at same position in P_{i+1}.")


def analysis_drop_block(num_blocks=6):
    print("(b) Loss of a Ciphertext Block")
    key, iv = os.urandom(16), os.urandom(16)
    P = os.urandom(num_blocks*BLOCK)
    C = aes_cbc_encrypt(key, iv, P)

    blocks = _split_blocks(C)
    lost = random.randrange(len(blocks))
    C_dropped = b"".join(blocks[:lost] + blocks[lost+1:])
    P_dec = aes_cbc_decrypt(key, iv, C_dropped)

    # Original plaintext blocks (before padding block)
    P_blocks = _split_blocks(P)
    Pdec_blocks = _split_blocks(P_dec[:len(P)])  # align to original length

    matches = [i for i,(a,b) in enumerate(zip(P_blocks, Pdec_blocks)) if a==b]
    print(f"- Dropped ciphertext block index: {lost}")
    print("- Blocks that still match original (indices):", matches)
    print("- Observation: After losing C_j, block j and all subsequent blocks fail (no resynchronization in CBC).")


def main():
    random.seed()
    analysis_bit_error()
    analysis_drop_block()

if __name__ == "__main__":
    main()