# voice-cloning
Voice Cloning with Coqui TTS (XTTS v2)
This project provides a simple command-line tool for voice cloning using Coqui TTS
 and the XTTS v2 multilingual model.
It allows you to generate speech in a target language that mimics the voice of a reference speaker from a WAV file.

Features

Clone a voice from a single reference .wav file.

Generate speech in multiple languages.

Runs on CPU or GPU (CUDA) automatically.

Simple command-line usage.

Requirements

Python 3.8+

PyTorch
 (with CUDA support for GPU acceleration)

Coqui TTS

Install dependencies:

pip install TTS torch

Usage
Clone a Voice
python clone_voice.py \
    --text "Hello, this is a cloned voice speaking!" \
    --speaker_wav path/to/reference.wav \
    --language en \
    --output cloned_output.wav

Arguments
Argument	Short	Required	Default	Description
--text	-t	✅ Yes	—	Text to synthesize.
--speaker_wav	-s	✅ Yes	—	Path to reference voice .wav file.
--language	-l	❌ No	en	Target language code (e.g., en, es, fr).
--output	-o	❌ No	output.wav	Output audio file path.
--device	-d	❌ No	auto-detected	Execution device: cpu or cuda.
Example

Clone a Spanish voice from an English speaker reference:

python clone_voice.py \
    --text "Hola, ¿cómo estás?" \
    --speaker_wav samples/voice.wav \
    --language es \
    --output cloned_spanish.wav

Notes

The reference file should be a clear WAV recording of the target speaker.

XTTS v2 supports multilingual synthesis; results may vary depending on the voice sample quality.

GPU is recommended for faster synthesis.

License

This project uses the Coqui TTS
 library, which is released under the MPL-2.0 license.
Please check the original repository for details.
