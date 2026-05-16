import os
import subprocess
import uuid

import torchaudio


MELO_PYTHON = "/home/theboss/ai/melo-test/.venv/bin/python"
MELO_SCRIPT = "/home/theboss/ai/melo-test/melo_generate.py"
COMFY_OUTPUT_DIR = "/home/theboss/ai/ComfyUI/output"


VOICES = [
    "EN-Default",
    "EN-US",
    "EN-BR",
    "EN_INDIA",
    "EN-AU",
    "ES",
    "FR",
    "ZH",
    "JP",
    "KR",
]


def _sanitize_filename(name: str) -> str:
    safe = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in name)
    return safe.strip("_") or "zetalvx_melo_output"


def _load_wav_as_comfy_audio(wav_path: str):
    waveform, sample_rate = torchaudio.load(wav_path)

    if waveform.ndim == 2:
        waveform = waveform.unsqueeze(0)

    return {
        "waveform": waveform,
        "sample_rate": sample_rate,
    }


class ZetalvxMeloGenerate:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello, this is a test generated with MeloTTS inside ComfyUI"
                }),
                "speaker": (VOICES, {
                    "default": "EN-US"
                }),
                "speed": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.05,
                }),
                "output_name": ("STRING", {
                    "default": "zetalvx_melo_output"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "AUDIO")
    RETURN_NAMES = ("audio_path", "selected_speaker", "audio")
    FUNCTION = "generate"
    CATEGORY = "ZetaLvx/Audio"
    OUTPUT_NODE = True

    def generate(self, text, speaker, speed, output_name):
        if not os.path.exists(MELO_PYTHON):
            raise FileNotFoundError(f"Melo python not found: {MELO_PYTHON}")

        if not os.path.exists(MELO_SCRIPT):
            raise FileNotFoundError(f"Melo script not found: {MELO_SCRIPT}")

        safe_name = _sanitize_filename(output_name)
        unique_id = uuid.uuid4().hex[:8]
        out_path = os.path.join(COMFY_OUTPUT_DIR, f"{safe_name}_{unique_id}.wav")

        cmd = [
            MELO_PYTHON,
            MELO_SCRIPT,
            "--text", text,
            "--speaker", speaker,
            "--speed", str(speed),
            "--out", out_path,
        ]

        print("[ZetalvxMeloTTS] Running:")
        print(" ".join(f'"{x}"' if " " in x else x for x in cmd))
        print(f"[ZetalvxMeloTTS] selected_speaker: {speaker}")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("[ZetalvxMeloTTS STDOUT]")
        print(result.stdout)

        if result.returncode != 0:
            print("[ZetalvxMeloTTS STDERR]")
            print(result.stderr)
            raise RuntimeError(f"MeloTTS generation failed:\n{result.stderr}")

        if not os.path.exists(out_path):
            raise FileNotFoundError(f"MeloTTS finished but output file was not found: {out_path}")

        audio = _load_wav_as_comfy_audio(out_path)

        return (out_path, speaker, audio)


NODE_CLASS_MAPPINGS = {
    "ZetalvxMeloGenerate": ZetalvxMeloGenerate
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZetalvxMeloGenerate": "Zetalvx MeloTTS Generate Audio"
}