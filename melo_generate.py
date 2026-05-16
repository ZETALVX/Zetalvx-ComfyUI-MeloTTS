import argparse
import os
import sys
from datetime import datetime

import torch
from melo.api import TTS


VOICE_LANGUAGE_MAP = {
    "EN-Default": "EN",
    "EN-US": "EN",
    "EN-BR": "EN",
    "EN_INDIA": "EN",
    "EN-AU": "EN",
    "ES": "ES",
    "FR": "FR",
    "ZH": "ZH",
    "JP": "JP",
    "KR": "KR",
}


def main():
    parser = argparse.ArgumentParser(description="External MeloTTS API wrapper")

    parser.add_argument("--text", required=True)
    parser.add_argument("--speaker", default="EN-US")
    parser.add_argument("--out", required=True)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--cuda", action="store_true")

    args = parser.parse_args()

    speaker = args.speaker.strip()

    if speaker not in VOICE_LANGUAGE_MAP:
        print(f"ERROR: unsupported speaker: {speaker}", file=sys.stderr)
        print(f"Supported speakers: {list(VOICE_LANGUAGE_MAP.keys())}", file=sys.stderr)
        sys.exit(1)

    language = VOICE_LANGUAGE_MAP[speaker]
    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    device = "cuda" if args.cuda and torch.cuda.is_available() else "cpu"

    print("MeloTTS API wrapper started")
    print("Time:", datetime.now().isoformat())
    print("Language:", language)
    print("Speaker:", speaker)
    print("Speed:", args.speed)
    print("Device:", device)
    print("Output:", out_path)

    try:
        model = TTS(language=language, device=device)
        speaker_ids = model.hps.data.spk2id

        print("Available speakers for this language:", speaker_ids)

        if speaker not in speaker_ids:
            print(
                f"ERROR: speaker '{speaker}' not available for language '{language}'",
                file=sys.stderr
            )
            sys.exit(1)

        speaker_id = speaker_ids[speaker]

        model.tts_to_file(
            args.text,
            speaker_id,
            out_path,
            speed=args.speed
        )

    except Exception as e:
        print(f"ERROR: MeloTTS generation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: generated {out_path}")


if __name__ == "__main__":
    main()