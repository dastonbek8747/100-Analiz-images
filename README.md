# AI Image Analyzer (OpenRouter)

> A Streamlit app that analyses images with vision models through the OpenRouter API.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)


## Features

- Upload an image and get a detailed description.
- Choose from several vision models on OpenRouter.
- Clean, styled interface.

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Vision LLM | OpenRouter vision models |
| Images | Pillow |

## Quick Start

```bash
git clone https://github.com/dastonbek8747/ai-image-analyzer-openrouter.git
cd ai-image-analyzer-openrouter
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # add OPENROUTER_API_KEY
streamlit run main.py
```

## Environment variables

| Variable | Meaning |
|---|---|
| `OPENROUTER_API_KEY` | OpenRouter API key. |

## License

MIT © 2026 Doston Sultonov.
