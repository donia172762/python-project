from __future__ import annotations
from typing import List

# AES parameters (fixed for AES-128)
Nb = 4   # columns in state (32-bit words)
Nk = 4   # key length in 32-bit words (AES-128 => 16 bytes)
Nr = 10  # number of rounds

# ----------------------------- GF(2^8) arithmetic -----------------------------
# All finite-field ops are implemented directly (no lookup tables),
# using the AES irreducible polynomial x^8 + x^4 + x^3 + x + 1 (0x11B).
MOD = 0x11B

def gf_xtime(a: int) -> int:
    """Multiply by x in GF(2^8) (i.e., by 2), then reduce modulo 0x11B if needed."""
    a <<= 1
    if a & 0x100:
        a ^= MOD
    return a & 0xFF

def gf_mul(a: int, b: int) -> int:
    """Generic GF(2^8) multiplication via the Russian peasant method."""
    res = 0
    x = a & 0xFF
    y = b & 0xFF
    for _ in range(8):
        if y & 1:
            res ^= x
        carry = x & 0x80
        x = (x << 1) & 0xFF
        if carry:
            x ^= 0x1B  # reduction step (0x11B without the implicit x^8 bit)
        y >>= 1
    return res & 0xFF

def rotl8(b: int, n: int) -> int:
    """Rotate 8-bit value left by n bits."""
    n %= 8
    return ((b << n) | (b >> (8 - n))) & 0xFF

def gf_pow(a: int, e: int) -> int:
    """Exponentiation in GF(2^8); used to compute multiplicative inverse."""
    r = 1
    base = a & 0xFF
    while e:
        if e & 1:
            r = gf_mul(r, base)
        base = gf_mul(base, base)
        e >>= 1
    return r & 0xFF

def gf_inv(a: int) -> int:
    """Multiplicative inverse in GF(2^8) (a^254). By convention inv(0) = 0."""
    if a == 0:
        return 0
    return gf_pow(a, 254)

# ----------------------------- S-box (algorithmic) ----------------------------
# Forward S-box via inverse + affine transform. No tables are stored.

def sub_byte(x: int) -> int:
    y = gf_inv(x)
    s = y ^ rotl8(y, 1) ^ rotl8(y, 2) ^ rotl8(y, 3) ^ rotl8(y, 4) ^ 0x63
    return s & 0xFF

# Inverse S-box computed by searching v in [0..255] s.t. sub_byte(v) == x.
# This is algorithmic and avoids embedding the inverse-table.
_inv_cache = {}

def inv_sub_byte(x: int) -> int:
    v = _inv_cache.get(x)
    if v is not None:
        return v
    for cand in range(256):
        if sub_byte(cand) == (x & 0xFF):
            _inv_cache[x] = cand
            return cand
    raise ValueError("Inverse S-box: byte not found")

# ----------------------------- State helpers ----------------------------------
# State is 4x4 bytes in column-major order: state[row][col].

def bytes_to_state(block16: bytes) -> List[List[int]]:
    assert len(block16) == 16
    state = [[0]*Nb for _ in range(4)]
    for i, b in enumerate(block16):
        c = i // 4
        r = i % 4
        state[r][c] = b
    return state

def state_to_bytes(state: List[List[int]]) -> bytes:
    out = bytearray(16)
    for c in range(Nb):
        for r in range(4):
            out[4*c + r] = state[r][c] & 0xFF
    return bytes(out)

# ----------------------------- Core transformations ---------------------------

def SubBytes(state):
    for r in range(4):
        for c in range(Nb):
            state[r][c] = sub_byte(state[r][c])

def InvSubBytes(state):
    for r in range(4):
        for c in range(Nb):
            state[r][c] = inv_sub_byte(state[r][c])

def ShiftRows(state):
    # Row r is rotated left by r bytes
    for r in range(1, 4):
        state[r] = state[r][r:] + state[r][:r]

def InvShiftRows(state):
    for r in range(1, 4):
        state[r] = state[r][-r:] + state[r][:-r]

def MixColumns(state):
    # Standard AES column mix (matrix × column in GF(2^8))
    for c in range(Nb):
        a0, a1, a2, a3 = state[0][c], state[1][c], state[2][c], state[3][c]
        state[0][c] = gf_mul(2, a0) ^ gf_mul(3, a1) ^ a2 ^ a3
        state[1][c] = a0 ^ gf_mul(2, a1) ^ gf_mul(3, a2) ^ a3
        state[2][c] = a0 ^ a1 ^ gf_mul(2, a2) ^ gf_mul(3, a3)
        state[3][c] = gf_mul(3, a0) ^ a1 ^ a2 ^ gf_mul(2, a3)

def InvMixColumns(state):
    # Inverse mix using constants {14,11,13,9}
    for c in range(Nb):
        a0, a1, a2, a3 = state[0][c], state[1][c], state[2][c], state[3][c]
        state[0][c] = gf_mul(14, a0) ^ gf_mul(11, a1) ^ gf_mul(13, a2) ^ gf_mul(9, a3)
        state[1][c] = gf_mul(9, a0) ^ gf_mul(14, a1) ^ gf_mul(11, a2) ^ gf_mul(13, a3)
        state[2][c] = gf_mul(13, a0) ^ gf_mul(9, a1) ^ gf_mul(14, a2) ^ gf_mul(11, a3)
        state[3][c] = gf_mul(11, a0) ^ gf_mul(13, a1) ^ gf_mul(9, a2) ^ gf_mul(14, a3)

def AddRoundKey(state, round_key_words: List[int]):
    # XOR 128-bit round key (4 words) into the state
    for c in range(Nb):
        word = round_key_words[c]
        state[0][c] ^= (word >> 24) & 0xFF
        state[1][c] ^= (word >> 16) & 0xFF
        state[2][c] ^= (word >> 8) & 0xFF
        state[3][c] ^= word & 0xFF

# ----------------------------- Key expansion ----------------------------------
# AES-128 generates 44 words (11 round keys × 4 words each).

def RotWord(w: int) -> int:
    return ((w << 8) & 0xFFFFFFFF) | ((w >> 24) & 0xFF)

def SubWord(w: int) -> int:
    return ((sub_byte((w >> 24) & 0xFF) << 24) |
            (sub_byte((w >> 16) & 0xFF) << 16) |
            (sub_byte((w >> 8) & 0xFF) << 8) |
            (sub_byte(w & 0xFF))) & 0xFFFFFFFF

def Rcon(i: int) -> int:
    # Rcon[i] = (2^{i-1}, 0, 0, 0)
    x = 1
    for _ in range(i-1):
        x = gf_xtime(x)
    return (x << 24) & 0xFFFFFFFF

def key_expansion(key16: bytes) -> List[int]:
    """Expand 16-byte key into 44 32-bit words."""
    assert len(key16) == 16
    w = [0] * (Nb * (Nr + 1))
    # Copy the original key (first 4 words)
    for i in range(Nk):
        w[i] = ((key16[4*i] << 24) | (key16[4*i+1] << 16) |
                (key16[4*i+2] << 8) | key16[4*i+3]) & 0xFFFFFFFF
    # Generate the rest
    for i in range(Nk, Nb*(Nr+1)):
        temp = w[i-1]
        if i % Nk == 0:
            temp = SubWord(RotWord(temp)) ^ Rcon(i//Nk)
        w[i] = (w[i-Nk] ^ temp) & 0xFFFFFFFF
    return w

# ----------------------------- Block cipher (AES-128) -------------------------

def aes_encrypt_block(block16: bytes, round_keys: List[int]) -> bytes:
    """Encrypt a single 16-byte block using expanded round keys."""
    state = bytes_to_state(block16)
    AddRoundKey(state, round_keys[0:4])
    for rnd in range(1, Nr):
        SubBytes(state)
        ShiftRows(state)
        MixColumns(state)
        AddRoundKey(state, round_keys[4*rnd:4*(rnd+1)])
    # Final round (no MixColumns)
    SubBytes(state)
    ShiftRows(state)
    AddRoundKey(state, round_keys[4*Nr:4*(Nr+1)])
    return state_to_bytes(state)

def aes_decrypt_block(block16: bytes, round_keys: List[int]) -> bytes:
    """Decrypt a single 16-byte block using expanded round keys."""
    state = bytes_to_state(block16)
    AddRoundKey(state, round_keys[4*Nr:4*(Nr+1)])
    for rnd in range(Nr-1, 0, -1):
        InvShiftRows(state)
        InvSubBytes(state)
        AddRoundKey(state, round_keys[4*rnd:4*(rnd+1)])
        InvMixColumns(state)
    InvShiftRows(state)
    InvSubBytes(state)
    AddRoundKey(state, round_keys[0:4])
    return state_to_bytes(state)

# ----------------------------- PKCS#7 padding ---------------------------------

def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len])*pad_len

def pkcs7_unpad(data: bytes, block_size: int = 16) -> bytes:
    if not data or len(data) % block_size != 0:
        raise ValueError("Invalid padded data length")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Invalid padding")
    if data[-pad_len:] != bytes([pad_len])*pad_len:
        raise ValueError("Bad PKCS#7 padding")
    return data[:-pad_len]

# ----------------------------- CBC mode ---------------------------------------

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def aes_cbc_encrypt(key16: bytes, iv16: bytes, plaintext: bytes) -> bytes:
    """AES-128 CBC with PKCS#7 padding."""
    if len(key16) != 16 or len(iv16) != 16:
        raise ValueError("Key and IV must be 16 bytes (128-bit)")
    rk = key_expansion(key16)
    pt = pkcs7_pad(plaintext, 16)
    out = bytearray()
    prev = iv16
    for i in range(0, len(pt), 16):
        block = xor_bytes(pt[i:i+16], prev)
        c = aes_encrypt_block(block, rk)
        out += c
        prev = c
    return bytes(out)

def aes_cbc_decrypt(key16: bytes, iv16: bytes, ciphertext: bytes) -> bytes:
    """AES-128 CBC decryption; expects ciphertext length multiple of 16."""
    if len(key16) != 16 or len(iv16) != 16 or len(ciphertext) % 16 != 0:
        raise ValueError("Key/IV must be 16 bytes and ciphertext multiple of 16")
    rk = key_expansion(key16)
    out = bytearray()
    prev = iv16
    for i in range(0, len(ciphertext), 16):
        c = ciphertext[i:i+16]
        pblk = aes_decrypt_block(c, rk)
        out += xor_bytes(pblk, prev)
        prev = c
    return pkcs7_unpad(bytes(out), 16)

# ----------------------------- Single-block CBC (NO padding) ------------------
# These helpers encrypt/decrypt exactly one 16-byte block using CBC chaining with IV,
# without applying PKCS#7 padding. They exist to satisfy the runner's
# "128-bit plaintext/ciphertext" requirement in the assignment.

def aes_cbc_encrypt_block_exact(key16: bytes, iv16: bytes, block16: bytes) -> bytes:
    if len(key16) != 16 or len(iv16) != 16 or len(block16) != 16:
        raise ValueError("Inputs must be exactly 16 bytes")
    rk = key_expansion(key16)
    x = xor_bytes(block16, iv16)
    return aes_encrypt_block(x, rk)


def aes_cbc_decrypt_block_exact(key16: bytes, iv16: bytes, block16: bytes) -> bytes:
    if len(key16) != 16 or len(iv16) != 16 or len(block16) != 16:
        raise ValueError("Inputs must be exactly 16 bytes")
    rk = key_expansion(key16)
    p = aes_decrypt_block(block16, rk)
    return xor_bytes(p, iv16)

# ----------------------------- Hex helpers for runner --------------------------

def hex_to_bytes(s: str) -> bytes:
    s = s.strip().lower().replace(" ", "")
    if len(s) % 2 != 0:
        s = "0" + s
    return bytes.fromhex(s)

def bytes_to_hex(b: bytes) -> str:
    return b.hex()