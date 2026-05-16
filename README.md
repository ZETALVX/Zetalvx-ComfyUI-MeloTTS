# Zetalvx-ComfyUI-MeloTTS

A ComfyUI custom node and local script integration for running **MeloTTS** inside a ComfyUI workflow.

This repository is part of the **ZETALVX AI Automation Lab** ecosystem: local-first, reproducible, modular AI tools for audio generation, voice workflows, and automation pipelines.

---

## Overview

`Zetalvx-ComfyUI-MeloTTS` provides a simple bridge between **ComfyUI** and a local **MeloTTS** installation.

The goal is to keep the TTS environment isolated from ComfyUI while still allowing ComfyUI workflows to generate speech audio through a dedicated custom node.

This approach is useful when you want to:

- generate speech locally
- keep TTS dependencies separated from the main ComfyUI environment
- integrate voice generation into larger AI workflows
- combine text generation, image generation, video generation and narration
- avoid cloud APIs where possible

---

## Features

- ComfyUI custom node for MeloTTS
- External Python environment support
- Local text-to-speech generation
- Output audio file path returned to ComfyUI
- Designed for modular AI workflows
- Suitable for narration, short dialogue, prototypes and automation pipelines

---

## Repository Structure

Recommended structure:

```text
Zetalvx-ComfyUI-MeloTTS/
├── README.md
├── LICENSE
├── requirements.txt
├── nodes/
│   └── zetalvx_melotts_node.py
├── scripts/
│   └── melotts_generate.py
└── examples/
    └── workflow_example.json
```

Depending on your implementation, the actual file names may be slightly different.

---

## Recommended Setup

The recommended setup is to use **two separate environments**:

1. ComfyUI environment  
2. MeloTTS dedicated environment  

This helps avoid dependency conflicts.

Example:

```bash
/home/theboss/ai/ComfyUI/venv311
/home/theboss/ai/melotts/.venv
```

The ComfyUI node should call the external MeloTTS script using the Python interpreter from the MeloTTS environment.

---

## Installation

### 1. Clone this repository into ComfyUI custom nodes

```bash
cd /home/theboss/ai/ComfyUI/custom_nodes
git clone https://github.com/ZETALVX/Zetalvx-ComfyUI-MeloTTS.git
```

Restart ComfyUI after cloning.

---

### 2. Prepare a dedicated MeloTTS environment

Example:

```bash
mkdir -p /home/theboss/ai/melotts
cd /home/theboss/ai/melotts

python3 -m venv .venv
source .venv/bin/activate
```

Install MeloTTS and required dependencies according to the official MeloTTS setup instructions.

If this repository includes a `requirements.txt`, install it with:

```bash
pip install -r requirements.txt
```

---

## ComfyUI Node Usage

Inside ComfyUI, add the MeloTTS node provided by this repository.

Typical inputs may include:

| Input | Description |
|---|---|
| `text` | Text to convert into speech |
| `melotts_python` | Full path to the MeloTTS virtual environment Python |
| `script_path` | Full path to the MeloTTS generation script |
| `language` | Language or voice preset, depending on your script |
| `speaker` | Speaker name or speaker ID, if supported |
| `speed` | Speech speed parameter |
| `output_dir` | Directory where generated audio files will be saved |

Example paths:

```text
melotts_python:
/home/theboss/ai/melotts/.venv/bin/python

script_path:
/home/theboss/ai/melotts/melotts_generate.py

output_dir:
/home/theboss/ai/ComfyUI/output/melotts
```

---

## Example CLI Test

Before using the ComfyUI node, test MeloTTS directly from terminal.

Example:

```bash
source /home/theboss/ai/melotts/.venv/bin/activate

python /home/theboss/ai/melotts/melotts_generate.py \
  --text "Hello, this is a local MeloTTS test." \
  --output /home/theboss/ai/ComfyUI/output/melotts/test.wav
```

If the CLI script works, then the ComfyUI node can call it reliably.

---

## Example Workflow

A typical workflow could be:

```text
Prompt / Text
   ↓
MeloTTS Node
   ↓
Generated WAV file
   ↓
Audio preview / video pipeline / narration workflow
```

This can be combined with:

- local LLMs
- ComfyUI text nodes
- image generation
- video generation
- subtitle generation
- local narration pipelines

---

## Troubleshooting

### Node does not appear in ComfyUI

Check that the repository is inside:

```bash
/home/theboss/ai/ComfyUI/custom_nodes/
```

Then restart ComfyUI.

Also check the ComfyUI terminal output for import errors.

---

### MeloTTS works in terminal but not in ComfyUI

Check that the node is using the correct external Python path:

```bash
/home/theboss/ai/melotts/.venv/bin/python
```

Do not use the ComfyUI Python environment unless you intentionally installed MeloTTS inside it.

---

### Audio file is not created

Check:

- the output directory exists
- ComfyUI has permission to write there
- the external script path is correct
- the CLI test works outside ComfyUI
- the MeloTTS model files are correctly downloaded

---

### Dependency conflicts

Use a dedicated MeloTTS environment.

Avoid installing MeloTTS directly inside the main ComfyUI environment unless you know the dependency versions are compatible.

---

## Notes

This project is designed as a practical local integration layer, not as a replacement for the official MeloTTS project.

The ComfyUI node acts as a bridge that launches an external script and returns the generated audio path back into the workflow.

---

## Credits

- MeloTTS project and contributors
- ComfyUI project and contributors
- ZETALVX AI Automation Lab workflow integration

---

## License

This repository is released under the license included in the `LICENSE` file.

Make sure to respect the licenses of:

- MeloTTS
- pretrained models
- datasets
- voices
- any third-party dependencies

If you use generated voices commercially, verify that the selected model, voice and dataset license allow commercial use.

---

## Author

Created by **ZETALVX – AI Automation Lab**

Local AI workflows, automation pipelines, ComfyUI integrations and open-source experiments.
