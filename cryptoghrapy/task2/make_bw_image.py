import sys
from PIL import Image

# Import AES primitives from our implementation
# (We also import pkcs7_pad; if it's not exported, we define a local fallback.)
try:
    from task2_aes import (
        key_expansion,
        aes_encrypt_block,
        aes_cbc_encrypt,
        pkcs7_pad,          # may or may not exist in the student's module
    )
except ImportError as e:
    raise

# Fallback in case pkcs7_pad wasn't exported (safe no-op if already imported)
try:
    pkcs7_pad  # type: ignore
except NameError:
    def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
        pad = block_size - (len(data) % block_size)
        if pad == 0:
            pad = block_size
        return data + bytes([pad]) * pad


BLOCK = 16  # AES block size (bytes)


def ecb_encrypt_bytes(key: bytes, data: bytes) -> bytes:
    """
    AES-128 ECB for arbitrary-length data:
    - PKCS#7 pad to a multiple of 16
    - encrypt block-by-block
    - truncate back to the original data length for visualization
    """
    rk = key_expansion(key)
    padded = pkcs7_pad(data, BLOCK)
    out = bytearray()
    for i in range(0, len(padded), BLOCK):
        out += aes_encrypt_block(padded[i:i+BLOCK], rk)
    # Keep image size exactly the same
    return bytes(out[:len(data)])


def cbc_encrypt_bytes(key: bytes, iv: bytes, data: bytes) -> bytes:
    """
    AES-128 CBC using our module's CBC (which pads internally).
    We truncate to the original data length to keep the image size unchanged.
    """
    ct = aes_cbc_encrypt(key, iv, data)  # PKCS#7 inside
    return ct[:len(data)]


def visualize_cipher(img_path: str) -> None:
    """
    Load an image, convert to grayscale, encrypt pixel bytes with ECB and CBC,
    and write out 'cipher_ecb.png' and 'cipher_cbc.png' using the SAME width/height.
    """
    # Read as grayscale so each pixel = 1 byte
    img = Image.open(img_path).convert("L")
    w, h = img.size
    px = img.tobytes()
    n = len(px)  # number of pixel bytes (must match w*h)

    # Fixed demo key/iv (128-bit) so results are reproducible in the report
    key = bytes.fromhex("00112233445566778899aabbccddeeff")
    iv  = bytes.fromhex("000102030405060708090a0b0c0d0e0f")

    # Encrypt pixel stream
    ecb_bytes = ecb_encrypt_bytes(key, px)
    cbc_bytes = cbc_encrypt_bytes(key, iv, px)

    # Rebuild images with EXACT same size; pass only the first n bytes
    Image.frombytes("L", (w, h), ecb_bytes[:n]).save("cipher_ecb.png")
    Image.frombytes("L", (w, h), cbc_bytes[:n]).save("cipher_cbc.png")

    print("Saved cipher_ecb.png and cipher_cbc.png")
    print("Key (hex): 00112233445566778899aabbccddeeff")
    print("IV  (hex): 000102030405060708090a0b0c0d0e0f")


def main():
    if len(sys.argv) < 2:
        print("Usage: python task2_cbc_image_exposure.py <input_image>")
        return
    visualize_cipher(sys.argv[1])


if __name__ == "__main__":
    main()