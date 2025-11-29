import random
import base64

class CryptoPipeline:
    def __init__(self):
        # FIXED: Increased Key Size
        # p=17, q=19, n=323 (Large enough for ASCII 255)
        # phi=288, e=5, d=173
        self.rsa_e = 5
        self.rsa_d = 173
        self.rsa_n = 323 

    # --- 1. RSA ---
    def apply_rsa(self, text, key_e, key_n):
        # Convert chars to integers, apply modular exponentiation
        encrypted = [pow(ord(c), key_e, key_n) for c in text]
        return " ".join(map(str, encrypted))

    def reverse_rsa(self, text_stream, key_d, key_n):
        try:
            codes = list(map(int, text_stream.split()))
            decrypted = [chr(pow(c, key_d, key_n)) for c in codes]
            return "".join(decrypted)
        except Exception as e:
            print(f"RSA Error: {e}")
            return text_stream 

    # --- 2. Monoalphabetic ---
    def apply_mono(self, text, key_map):
        return "".join([key_map.get(c, c) for c in text])

    def reverse_mono(self, text, key_map):
        reverse_map = {v: k for k, v in key_map.items()}
        return "".join([reverse_map.get(c, c) for c in text])

    # --- 3. Transposition ---
    def apply_transposition(self, text):
        return text[::-1]

    def reverse_transposition(self, text):
        return text[::-1]

    # --- 4. Vernam ---
    def apply_vernam(self, text, otp):
        res = []
        for i in range(len(text)):
            t_char = text[i]
            k_char = otp[i % len(otp)]
            # XOR operation
            res.append(chr(ord(t_char) ^ ord(k_char)))
        return "".join(res)

    # --- 5. Playfair (Simplified) ---
    def apply_playfair(self, text, key):
        return text.swapcase()

    def reverse_playfair(self, text, key):
        return text.swapcase() 

    # --- 6. Vigenere ---
    def apply_vigenere(self, text, key):
        res = []
        key_idx = 0
        for char in text:
            # Only shift standard letters to avoid corrupting Vernam output
            if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
                shift = ord(key[key_idx % len(key)].upper()) - 65
                if char.isupper():
                    res.append(chr((ord(char) - 65 + shift) % 26 + 65))
                else:
                    res.append(chr((ord(char) - 97 + shift) % 26 + 97))
                key_idx += 1
            else:
                res.append(char)
        return "".join(res)

    def reverse_vigenere(self, text, key):
        res = []
        key_idx = 0
        for char in text:
            if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
                shift = ord(key[key_idx % len(key)].upper()) - 65
                if char.isupper():
                    res.append(chr((ord(char) - 65 - shift) % 26 + 65))
                else:
                    res.append(chr((ord(char) - 97 - shift) % 26 + 97))
                key_idx += 1
            else:
                res.append(char)
        return "".join(res)

    # --- PIPELINES ---
    def full_encryption_pipeline(self, plaintext):
        # 1. Generate Keys
        mono_key = {chr(i): chr((i + 1) % 256) for i in range(256)}
        # OTP must cover the length of the intermediate data
        otp_key = "".join([chr(random.randint(33, 126)) for _ in range(len(plaintext) * 10)])
        vig_key = "KEYWORD"
        
        # 2. Apply Layers
        step1 = self.apply_rsa(plaintext, self.rsa_e, self.rsa_n)
        step2 = self.apply_mono(step1, mono_key)
        step3 = self.apply_transposition(step2)
        
        current_otp = otp_key[:len(step3)]
        step4 = self.apply_vernam(step3, current_otp)
        
        step5 = self.apply_playfair(step4, "PLAYFAIR")
        raw_cipher = self.apply_vigenere(step5, vig_key)

        # FIXED: Encode to Base64 to make it safe for network/text files
        safe_cipher = base64.b64encode(raw_cipher.encode('latin1')).decode('utf-8')

        keys = {
            "rsa_d": self.rsa_d, "rsa_n": self.rsa_n,
            "mono": mono_key,
            "otp": current_otp,
            "vig": vig_key
        }
        return safe_cipher, keys

    def full_decryption_pipeline(self, safe_ciphertext, keys):
        # FIXED: Decode from Base64 first
        try:
            raw_ciphertext = base64.b64decode(safe_ciphertext).decode('latin1')
        except:
            return "Error: Corrupted Cipher File"

        # Reverse Layers
        step1 = self.reverse_vigenere(raw_ciphertext, keys["vig"])
        step2 = self.reverse_playfair(step1, "PLAYFAIR")
        step3 = self.apply_vernam(step2, keys["otp"])
        step4 = self.reverse_transposition(step3)
        step5 = self.reverse_mono(step4, keys["mono"])
        final_text = self.reverse_rsa(step5, keys["rsa_d"], keys["rsa_n"])
        
        return final_text