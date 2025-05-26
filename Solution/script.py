import numpy as np
from scipy.io import wavfile
import base64

# === Step 1: Read the FSK Signal ===
rate, data = wavfile.read("challenge_fsk.wav")

# === Step 2: Define FSK parameters ===
f1, f2 = 1000, 2000  # Frequencies for bit 0 and 1
bit_duration = 0.1  # seconds per bit
samples_per_bit = int(rate * bit_duration)

# === Step 3: Extract binary bits based on frequency ===
binary_string = ""
for i in range(0, len(data), samples_per_bit):
    segment = data[i:i + samples_per_bit]
    if len(segment) < samples_per_bit:
        break
    freq = np.fft.fftfreq(len(segment), d=1/rate)
    fft_result = np.abs(np.fft.fft(segment))
    dominant_freq = abs(freq[np.argmax(fft_result)])

    if abs(dominant_freq - f1) < 50:
        binary_string += "0"
    elif abs(dominant_freq - f2) < 50:
        binary_string += "1"

print("[+] Extracted Binary:")
print(binary_string)

# === Step 4: Convert Binary to ASCII (Base64 string) ===
decoded_text = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
print("\n[+] Decoded Base64 String:")
print(decoded_text)

# === Step 5: Base64 Decode and XOR Decrypt ===
try:
    decoded_encrypted = base64.b64decode(decoded_text).decode()
except Exception as e:
    print("\n[!] Base64 decoding failed:", e)
    exit()

key = "WindowsSDR"  # XOR key
decrypted_flag = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(decoded_encrypted))

print("\n✅ Decrypted Flag:")
print(decrypted_flag)
