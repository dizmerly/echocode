# echocode
Local Speech to Code

## Requirements

- A Mac with Apple Silicon and access to Metal for MLX inference.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python and dependency management.
- Python 3.12 or newer. The setup below uses Python 3.12.
- FFmpeg for audio decoding.

If you use Homebrew, install the tools with:

```bash
brew install uv ffmpeg
```

## Set up the project

From the repository root:

```bash
uv python install 3.12
uv sync --python 3.12 --locked
```

This creates the project's `.venv` and installs the dependencies recorded in
`uv.lock`. There is no separate build step for the current Python scripts.
`uv run` uses the project environment, so activating `.venv` is optional.

## Hugging Face authentication (optional)

The example downloads `mlx-community/parakeet-tdt-0.6b-v3` on its first run.
Subsequent runs reuse the cached model. Internet access is required for the
initial download.

To avoid the unauthenticated download warning and get higher rate limits,
create a **Read** token in your
[Hugging Face token settings](https://huggingface.co/settings/tokens), then log in:

```bash
uv run hf auth login
```

Paste the token when prompted. Adding it as a Git credential is unnecessary
for this example. Keep the token out of source files and Git.

## Run the transcription example

Place an audio file named `audio_file.wav` in the repository root, then run:

```bash
uv run python src/example.py
```

The example reads that file in one-second chunks and prints the current
transcription as it processes each chunk. It simulates streaming from a file;
it does not capture microphone input. To use another file, change the path
passed to `load_audio` in `src/example.py`.

You can also transcribe a file directly with the installed Parakeet CLI:

```bash
uv run parakeet-mlx audio_file.wav --output-format txt
```

The project uses the [PyPI parakeet-mlx API](https://pypi.org/project/parakeet-mlx/),
including `from_pretrained` and `model.transcribe_stream`.

## Update dependencies

To upgrade Parakeet and update the dependency files:

```bash
uv add parakeet-mlx -U
```

Commit both `pyproject.toml` and `uv.lock` when changing dependencies so other
checkouts can install the same versions with `uv sync --locked`.
