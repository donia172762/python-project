from tqdm import tqdm

class LFSR:
    def __init__(self, name, length, taps, clock_bit, state):
        self.name = name
        self.length = length
        self.taps = taps
        self.clock_bit = clock_bit
        self.state = [int(b) for b in state]

    def shift(self):
        feedback = 0
        for t in self.taps:
            feedback ^= self.state[t]
        out_bit = self.state[-1]
        self.state = [feedback] + self.state[:-1]
        return out_bit

    def get_clock_bit(self):
        return self.state[self.clock_bit]

    def get_output_bit(self):
        return self.state[-1]

def create_lfsrs(x_state, y_state, z_state):
    LFSR_X = LFSR("X", 19, [13, 16, 17, 18], 8, x_state)
    LFSR_Y = LFSR("Y", 22, [20, 21], 10, y_state)
    LFSR_Z = LFSR("Z", 23, [7, 20, 21, 22], 10, z_state)
    return LFSR_X, LFSR_Y, LFSR_Z

def majority(a, b, c):
    return 1 if a + b + c >= 2 else 0

def generate_keystream(x_state, y_state, z_state, num_bits):
    X, Y, Z = create_lfsrs(x_state, y_state, z_state)
    keystream = []
    for _ in range(num_bits):
        m = majority(X.get_clock_bit(), Y.get_clock_bit(), Z.get_clock_bit())
        if X.get_clock_bit() == m:
            X.shift()
        if Y.get_clock_bit() == m:
            Y.shift()
        if Z.get_clock_bit() == m:
            Z.shift()
        ks_bit = X.get_output_bit() ^ Y.get_output_bit() ^ Z.get_output_bit()
        keystream.append(ks_bit)
    return keystream

def text_to_bits(text):
    return [int(b) for char in text.encode('utf-8') for b in f"{char:08b}"]

def find_correct_y(x_state, z_state, target_keystream):
    def format_state(bits):
        return bits.zfill(22)

    for i in tqdm(range(2**22), desc="Brute-forcing Y"):
        y_candidate = format_state(bin(i)[2:])
        ks = generate_keystream(x_state, y_candidate, z_state, len(target_keystream))
        if ks == target_keystream:
            print(f"✅ Recovered Y state: {y_candidate}")
            with open("recovered_y_state.txt", "w") as f:
                f.write(y_candidate)
            return y_candidate

    print("❌ No matching Y state found.")
    return None

if __name__ == "__main__":
    with open("initial_states.txt") as f:
        x_state = f.readline().strip()
        z_state = f.readline().strip()

    with open("known_plaintext.txt") as f:
        known_plaintext = f.read().strip()

    # ✅ تعديل مهم هنا: قراءة الـ ciphertext على أنه بتات نصية '0' و '1'
    with open("ciphertext.bin", "r") as f:
        ciphertext_bits = [int(b) for b in f.read().strip()]

    plaintext_bits = text_to_bits(known_plaintext)

    # استخدم فقط نفس عدد البتات من plaintext
    ciphertext_bits = ciphertext_bits[:len(plaintext_bits)]

    # حساب keystream من XOR
    target_keystream = [p ^ c for p, c in zip(plaintext_bits, ciphertext_bits)]

    print("Known plaintext length:", len(known_plaintext))
    print("Target keystream length (bits):", len(target_keystream))
    print("First 32 bits of keystream:", target_keystream[:32])

    # جرّب على أول 32 بت لتسريع المطابقة
    find_correct_y(x_state, z_state, target_keystream[:32])
