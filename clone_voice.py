
import argparse
import os
import sys
from typing import Optional

try:
    import torch
    _HAS_CUDA = torch.cuda.is_available()
except Exception:
    torch = None
    _HAS_CUDA = False

try:
    from torch.serialization import add_safe_globals
except Exception:
    add_safe_globals = None

try:
    from TTS.config.shared_configs import BaseDatasetConfig
except Exception:
    BaseDatasetConfig = None

try:
    from TTS.tts.configs.xtts_config import XttsConfig
except Exception:
    XttsConfig = None

try:
    from TTS.tts.models.xtts import XttsAudioConfig
except Exception:
    XttsAudioConfig = None

from TTS.api import TTS

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"


def clone_voice(text: str, speaker_wav: str, language: str, output: str, device: Optional[str] = None) -> None:
    """Clone a voice using XTTS v2 and synthesize text to a WAV file."""
    if not os.path.isfile(speaker_wav):
        raise FileNotFoundError(f"Reference voice file not found: {speaker_wav}")

    dev = device or ("cuda" if _HAS_CUDA else "cpu")

    print(f"[INFO] Loading model '{MODEL_NAME}' on device: {dev} ...", flush=True)

    safe_classes = []
    for cls in (BaseDatasetConfig, XttsConfig, XttsAudioConfig):
        if cls:
            safe_classes.append(cls)

    try:
        from TTS.tts.models.xtts import XttsArgs
        safe_classes.append(XttsArgs)
    except Exception:
        pass

    if add_safe_globals and safe_classes:
        try:
            add_safe_globals(safe_classes)
            print(f"[INFO] Registered safe globals: {[c.__name__ for c in safe_classes]}")
        except Exception as e:
            print(f"[WARN] Could not register safe globals: {e}")

    # --- Load TTS model ---
    tts = TTS(MODEL_NAME).to(dev)

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    print(f"[INFO] Generating audio => {output}", flush=True)

    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language=language,
        file_path=output,
    )

    print("[SUCCESS] Done.")



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clone a voice with Coqui TTS XTTS v2 and synthesize text to a WAV file.",
    )
    parser.add_argument("--text", "-t", required=True, help="Text to synthesize.")
    parser.add_argument("--speaker_wav", "-s", required=True, help="Path to the reference voice WAV file.")
    parser.add_argument("--language", "-l", default="en", help="Target language code (default: en).")
    parser.add_argument("--output", "-o", default="output.wav", help="Output WAV file path (default: output.wav).")
    parser.add_argument(
        "--device",
        "-d",
        choices=["cpu", "cuda"],
        help="Execution device. Defaults to CUDA if available, otherwise CPU.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        clone_voice(
            text=args.text,
            speaker_wav=args.speaker_wav,
            language=args.language,
            output=args.output,
            device=args.device,
        )
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
