import numpy as np
import sounddevice as sd

print(sd.query_devices())
print("Default i/o device IDs", sd.default.device)

print("Speak for five seconds...")
audio = sd.rec(
    frames = 5 * 16000,
    samplerate=16000,
    channels=1,
    dtype="float32",
    blocking=True,
)

print("Shape:", audio.shape)
print("Peak:", float(np.max(np.abs(audio))))
print("RMS:", float(np.sqrt(np.mean(audio ** 2))))


