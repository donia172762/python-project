from task2_aes import (
    hex_to_bytes, bytes_to_hex,
    aes_cbc_encrypt_block_exact, aes_cbc_decrypt_block_exact,
)

HEX_DIGITS = set("0123456789abcdefABCDEF")


def _read_hex_exact(prompt: str, bits: int) -> bytes:
    """Read an exact-length hex string (e.g., 128 bits => 32 hex chars)."""
    req_len = bits // 4
    s = input(prompt).strip().replace(" ", "")
    if len(s) != req_len or any(ch not in HEX_DIGITS for ch in s):
        raise ValueError(f"Expected exactly {req_len} hex characters ({bits}-bit).")
    return hex_to_bytes(s)


def main():
    op = input("Operation [E=Encrypt / D=Decrypt]: ").strip().upper()
    key = _read_hex_exact("AES key (128-bit, hex): ", 128)
    iv  = _read_hex_exact("IV (128-bit, hex): ", 128)

    if op == 'E':
        pt = _read_hex_exact("Plaintext (128-bit, hex): ", 128)
        ct = aes_cbc_encrypt_block_exact(key, iv, pt)
        print("OUTPUT (ciphertext, hex):", bytes_to_hex(ct))
    elif op == 'D':
        ct = _read_hex_exact("Ciphertext (128-bit, hex): ", 128)
        pt = aes_cbc_decrypt_block_exact(key, iv, ct)
        print("OUTPUT (plaintext, hex):", bytes_to_hex(pt))
    else:
        print("Invalid choice. Use E or D.")

if __name__ == "__main__":
    main()