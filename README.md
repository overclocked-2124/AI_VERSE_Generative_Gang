# Voice Assistant AI Bot with Multilingual Support

This project implements an AI bot with voice assistant capabilities that can listen to user queries in any language and respond in the same language. The bot has a customizable character and backstory, maintaining its persona throughout interactions.

## Features

- Speech-to-Speech (S2S) system
- Multilingual support for both input and output
- Character-based responses with consistent persona
- Local LLM support using Ollama
- Web interface built with Flask

## Prerequisites

- Python 3.8+
- Ollama installed on your machine
- Sufficient disk space for LLM models
- Microphone for voice input
- Speakers for voice output

## Installation

### 1. Install Ollama

First, you need to install Ollama to run LLMs locally:

**For Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**For macOS/Windows:**
Visit [ollama.com](https://ollama.com/) to download and install the software.

### 2. Download an LLM Model

After installing Ollama, pull a model:
```bash
ollama pull gemma:2b
```

You can choose different models based on your needs and hardware capabilities.

### 3. Clone the Repository

```bash
git clone https://github.com/yourusername/voice-assistant-ai-bot.git
cd voice-assistant-ai-bot
```

### 4. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## Project Structure
voice-assistant-ai-bot/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── speech.py
│   ├── llm.py
│   ├── character.py
│   └── utils.py
├── static/
│   ├── css/
│   │   └── main.css
│   └── js/
│       └── app.js
├── templates/
│   ├── index.html
│   └── includes/
│       └── header.html
├── run.py
├── requirements.txt
└── README.md

## Running the Application

### 1. Start Ollama with your chosen model

```bash
ollama run gemma:2b
```

This will start the Ollama service with the specified model.

### 2. Start the Flask Application

```bash
python run.py
```

The application will be available at http://127.0.0.1:5000/ by default.

## Usage

1. Open the web interface in your browser
2. Click the microphone button to start speaking
3. Ask your question in any language
4. The AI bot will process your query and respond in the same language while maintaining its character

## Customizing the Bot's Character

You can modify the bot's character and backstory by editing the `character.py` file in the app directory. The file contains personality traits, speech patterns, and backstory elements that define how the bot responds to queries.

## Troubleshooting

- **Ollama not responding**: Ensure Ollama is running in a separate terminal window
- **Microphone not working**: Check your browser permissions for microphone access
- **Slow responses**: Consider using a smaller or more optimized LLM model

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
Answer from Perplexity: pplx.ai/share# AI_VERSE_Generative_Gang
This is the project made for the AI Verse Hackathon
