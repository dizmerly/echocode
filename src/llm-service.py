from pathlib import Path

from mlx_audio.stt import load
from mlx_audio.stt.models.nemotron_asr import Model as NemotronModel

MODEL_ID = "mlx-community/nemotron-3.5-asr-streaming-0.6b"

# download the model on first run, reusue from cache
model = load(MODEL_ID)

if not isinstance(model, NemotronModel):
    raise TypeError(f"Expect NemotronModel, got {type(model).__name__}")

# Intake audio via microphone via keypress.
# Location of keypress should be stored (i.e. line for code placement)
audio_path = Path("test2.m4a")
if not audio_path.is_file():
    raise FileNotFoundError(f"Audio file not found: {audio_path.resolve()}")

# Transcribe a audio file
result = model.generate(
    str(audio_path),
    language="en-US",
)

# Store transcription for later
print(result.text)

# Stage the transcription for implementation

# Pass transcription to model to write a line



# LLM model writes to file in given file 