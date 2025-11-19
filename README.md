# ElevenLabs Speech-to-Text Converter

This project provides a solution for transcribing audio files using the ElevenLabs Speech-to-Text API. It includes both a Command Line Interface (CLI) and a Flask Web Application.

## Features

- **Web Interface**: A user-friendly web interface built with Flask.
- **CLI Tool**: A simple command-line script for quick transcriptions.
- **Local File Support**: Upload and transcribe audio files from your local machine.
- **URL Support**: Transcribe audio directly from a web URL.

## Prerequisites

- Python 3.8+
- An [ElevenLabs API Key](https://elevenlabs.io/)

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/aivisbr/StartSchool_API_task2.git
    cd StartSchool_API_task2
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Set up environment variables:
    - Rename `.env.example` to `.env`.
    - Add your ElevenLabs API key to `.env`:
      ```
      ELEVENLABS_API_KEY=your_api_key_here
      ```

## Usage

### Web Application (Recommended)

1.  Run the Flask app:
    ```bash
    python app.py
    ```
2.  Open your browser and navigate to `http://127.0.0.1:5000`.

### CLI Tool

1.  Run the script:
    ```bash
    python stt_converter.py
    ```
2.  Follow the on-screen prompts to choose between local file or URL.

## License

This project is open source.