import sys, os
from PIL import Image
from task2_aes import key_expansion, aes_encrypt_block, aes_cbc_encrypt

BLOCK = 16

def _pad16(b: bytes) -> bytes:
    # Simple zero padding for pixel array (visualization only)
    r = len(b) % BLOCK
    return b if r==0 else b + bytes(BLOCK - r)

def _aes_ecb_encrypt_no_pad(key: bytes, data: bytes) -> bytes:
    rk = key_expansion(key)
    out = bytearray()
    for i in range(0, len(data), BLOCK):
        out += aes_encrypt_block(data[i:i+BLOCK], rk)
    return bytes(out)

def visualize_cipher(img_path: str):
    img = Image.open(img_path).convert('L')  # grayscale
    px = bytes(img.tobytes())

    key = os.urandom(16)
    iv  = os.urandom(16)

    # Prepare multiples of 16 for block ciphers
    px16 = _pad16(px)

    # ECB (for comparison)
    cte = _aes_ecb_encrypt_no_pad(key, px16)
    e_img = Image.frombytes('L', (img.width, (len(cte)+img.width-1)//img.width), cte[:len(px)])
    e_img = e_img.crop((0,0,img.width,img.height))
    e_img.save('cipher_ecb.png')

    # CBC using our module (with PKCS#7); truncate to original pixel count for visualization
    ctc = aes_cbc_encrypt(key, iv, px16)
    c_img = Image.frombytes('L', (img.width, (len(ctc)+img.width-1)//img.width), ctc[:len(px)])
    c_img = c_img.crop((0,0,img.width,img.height))
    c_img.save('cipher_cbc.png')

    print("Saved: cipher_ecb.png (patterns visible) and cipher_cbc.png (noise-like, patterns suppressed).")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python task2_cbc_image_exposure.py <input_image.png>")
        sys.exit(1)
    visualize_cipher(sys.argv[1])