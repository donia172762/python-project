from task2_aes import (
    key_expansion, aes_encrypt_block, aes_decrypt_block,
    aes_cbc_encrypt, aes_cbc_decrypt
)

# Helpers for CBC without padding (for NIST vectors)
def _cbc_encrypt_no_pad(key, iv, pt):
    assert len(pt) % 16 == 0
    rk = key_expansion(key)
    ct = bytearray()
    prev = iv
    for i in range(0, len(pt), 16):
        blk = bytes(a ^ b for a,b in zip(pt[i:i+16], prev))
        c = aes_encrypt_block(blk, rk)
        ct += c
        prev = c
    return bytes(ct)

def _cbc_decrypt_no_pad(key, iv, ct):
    assert len(ct) % 16 == 0
    rk = key_expansion(key)
    out = bytearray()
    prev = iv
    for i in range(0, len(ct), 16):
        c = ct[i:i+16]
        p = aes_decrypt_block(c, rk)
        out += bytes(a ^ b for a,b in zip(p, prev))
        prev = c
    return bytes(out)


def main():
    import os
    # Test 1: FIPS-197
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    pt  = bytes.fromhex("00112233445566778899aabbccddeeff")
    exp = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
    rk   = key_expansion(key)
    ct   = aes_encrypt_block(pt, rk)
    print("FIPS-197 ECB 1-block:", "PASS" if ct==exp else "FAIL")

    # Test 2: SP 800-38A CBC
    key2 = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    iv2  = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    pt2  = bytes.fromhex(
        "6bc1bee22e409f96e93d7e117393172a"
        "ae2d8a571e03ac9c9eb76fac45af8e51"
        "30c81c46a35ce411e5fbc1191a0a52ef"
        "f69f2445df4f9b17ad2b417be66c3710"
    )
    exp2 = bytes.fromhex(
        "7649abac8119b246cee98e9b12e9197d"
        "5086cb9b507219ee95db113a917678b2"
        "73bed6b8e3c1743b7116e69e22229516"
        "3ff1caa1681fac09120eca307586e1a7"
    )
    ct2 = _cbc_encrypt_no_pad(key2, iv2, pt2)
    ok2 = (ct2 == exp2) and (_cbc_decrypt_no_pad(key2, iv2, ct2) == pt2)
    print("SP800-38A CBC 4-blocks:", "PASS" if ok2 else "FAIL")

    # Test 3: Random CBC round-trip with PKCS#7
    k = os.urandom(16); iv = os.urandom(16); pt = os.urandom(37)
    ct = aes_cbc_encrypt(k, iv, pt)
    ok3 = (aes_cbc_decrypt(k, iv, ct) == pt)
    print("CBC PKCS#7 round-trip:", "PASS" if ok3 else "FAIL")

if __name__ == "__main__":
    main()