from mlx_audio.stt.models.nemotron_asr import Model as NemotronModel
from mlx_audio.stt import load



from queue import Empty, SimpleQueue
from pathlib import Path
import sounddevice as sd
import numpy as np
import time

MODEL_ID = "mlx-community/nemotron-3.5-asr-streaming-0.6b"
# download the model on first run, reusue from cache
model = load(MODEL_ID)

if not isinstance(model, NemotronModel):
    raise TypeError(f"Expect NemotronModel, got {type(model).__name__}")
# Intake audio via microphone via keypress.
# Location of keypress should be stored (i.e. line for code placement)
session = model.create_streaming_session(language="en-US")
transcript_parts: list[str] = []
# Transfer microphone sample to main thread
audio_queue: SimpleQueue[np.ndarray] = SimpleQueue()


# Callback function whenever audio is recieved
def on_audio(indata, frames, time_info, status):
    # sound device reuses indata, copy before returning
    microphone_channel = indata[:, 0]
    saved_samples = microphone_channel.copy()
    audio_queue.put(saved_samples)

def consume_audio(max_chunks=8):
    for _ in range(max_chunks):
        try:
            samples = audio_queue.get_nowait()
        except Empty:
            break
        session.feed(samples)
        
def print_fragments(fragments):
    # Streaming results fed into the list as fragments
    transcript_parts.extend(fragments)
    if fragments:
        print("".join(fragments), end="", flush=True)

print("Listening... <CTRL+C to stop>")

# Transcribe a audio file
try:
    with sd.InputStream(
        samplerate=session.input_sample_rate,
        channels=1,
        dtype="float32",
        latency="low",
        callback=on_audio,
    ):
        while not session.done:
            consume_audio()
            # return text fragments, not full transcript
            fragments = session.step(max_decode_tokens=32)
            print_fragments(fragments)
            time.sleep(0.005)

except KeyboardInterrupt:
    print("\nStopped Listening...", flush=True)
    
# Cleans up Audio buffer
while not audio_queue.empty():
    consume_audio()
    fragments = session.step(max_decode_tokens=32)
    print_fragments(fragments)

session.close()

# Cleans up model's buffer
# Store transcription for later
while not session.done:
    fragments = session.step(max_decode_tokens=32)
    print_fragments(fragments)

print("\nFinished with: \n", "".join(transcript_parts), flush=True)

# Stage the transcription for implementation



# Pass transcription to model to write a line


# LLM model writes to file in given file
