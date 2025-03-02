# MP3 to Anki Deck Converter

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Downloading Corresponding `.lrc` Files for a Song](#1-downloading-corresponding-lrc-files-for-a-song)
  - [2. Creating an Anki Deck Based on an MP3 Song](#2-creating-an-anki-deck-based-on-an-mp3-song)
  - [3. Creating a Context File for an Anki Deck](#3-creating-a-context-file-for-an-anki-deck)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

The **MP3 to Anki Deck Converter** is a Python-based tool designed to help language learners and music enthusiasts create interactive Anki decks from MP3 songs. It automates the process of downloading synchronized lyrics, translating them, splitting audio clips, and compiling everything into an Anki deck for effective memorization and learning.

## Features

- **Download Lyrics:** Automatically fetches `.lrc` files (synchronized lyrics) for your MP3 songs.
- **Anki Deck Creation:** Splits MP3 files into individual clips and generates corresponding Anki flashcards with original lyrics and translations.
- **Context File Generation:** Creates context files containing all cards in a deck for easy reference and management.
- **Environment Management:** Utilizes environment variables for secure API key management.
- **Media Handling:** Manages audio clips and Anki deck packages efficiently.

## Prerequisites

Before using the scripts, ensure you have the following installed:

- **Python 3.7+**
- **Anki** (for managing decks)
- **AnkiConnect Add-on:** Install the AnkiConnect add-on in Anki (Add-on code: `2055492159`)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/AnkiGPT.git
   cd AnkiGPT
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the project root with the following content:
   ```dotenv
   DEEPSEEK_API_KEY=your_deepseek_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

   Replace `your_deepseek_api_key` and `your_openai_api_key` with your actual API keys.

## Usage

### 1. Downloading Corresponding `.lrc` Files for a Song

The `sync_lyrics.py` script automates the process of fetching synchronized `.lrc` files for your MP3 songs.

**Steps:**

1. **Prepare Your MP3 Files:**

   Ensure your MP3 files follow the naming convention:
   ```
   Song Name - Artist Name.mp3
   ```
   *Example:*
   ```
   Again - Yui.mp3
   Departure - Masatoshi Ono.mp3
   ```

2. **Run the Script:**
   ```bash
   python sync_lyrics.py
   ```

   **Script Details:**
   ```python:sync_lyrics.py
   ```

   The script scans the current directory for MP3 files, extracts the track and artist names, fetches the corresponding lyrics using the `syncedlyrics` library, and saves them as `.lrc` files in the specified output directory.

### 2. Creating an Anki Deck Based on an MP3 Song

The `lyrics_to_anki.py` script takes an MP3 file and its corresponding `.lrc` file to create an Anki deck with flashcards containing audio clips, original lyrics, and their English translations.

**Steps:**

1. **Ensure `.lrc` Files are Available:**

   Make sure you've downloaded the `.lrc` files using the `sync_lyrics.py` script.

2. **Run the Script:**
   ```bash
   python lyrics_to_anki.py "Song Name - Artist Name"
   ```

   *Example:*
   ```bash
   python lyrics_to_anki.py "Again - Yui"
   ```

   **Script Details:**
   ```python:lyrics_to_anki.py
   ```

   The script performs the following:
   - Splits the MP3 file into individual audio clips based on the timestamps in the `.lrc` file.
   - Translates the original lyrics to English using the DeepSeek API.
   - Generates an Anki deck (`.apkg` file) containing flashcards with audio, original lyrics, and translations.

3. **Locate the Generated Anki Deck:**

   The deck will be saved in the `assets/anki_decks/` directory with the name `Song Name - Artist Name.apkg`.

4. **Import the Deck into Anki:**

   Open Anki, go to `File` > `Import`, and select the generated `.apkg` file to add it to your Anki collection.

### 3. Creating a Context File for an Anki Deck

The `anki_utils.py` script provides utilities to manage and create context files for your Anki decks.

**Steps:**

1. **Run the Script:**
   ```bash
   python anki_utils.py
   ```

   **Script Details:**
   ```python:anki_utils.py
   ```

   The script performs the following:
   - Connects to Anki via the AnkiConnect API.
   - Retrieves all cards from specified decks.
   - Generates context files (`.txt`) containing detailed information about each card for reference.

2. **Locate the Generated Context Files:**

   The context files will be saved in the `assets/anki_context_files/` directory with filenames based on the deck names.

## Configuration

- **Environment Variables:**

  The application relies on several API keys and directory configurations managed through environment variables. Ensure your `.env` file includes the necessary keys:

  ```dotenv
  DEEPSEEK_API_KEY=your_deepseek_api_key
  OPENAI_API_KEY=your_openai_api_key
  ```

- **Directory Structure:**

  - `assets/music/` - Contains your MP3 files.
  - `assets/audio_clips/` - Stores the split audio clips.
  - `assets/anki_decks/` - Stores the generated Anki deck packages.
  - `assets/anki_context_files/` - Stores the generated context files.

  These directories are automatically created if they do not exist.

## Project Structure

```
AnkiGPT/
├── assets/
│   ├── anki_decks/
│   ├── anki_context_files/
│   ├── audio_clips/
│   └── music/
├── .gitignore
├── anki_utils.py
├── lyrics_to_anki.py
├── sync_lyrics.py
├── README.md
├── requirements.txt
└── .env
```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m "Add YourFeature"
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/YourFeature
   ```
5. **Open a Pull Request**

Please ensure your code adheres to the project's coding standards and includes appropriate documentation.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [syncedlyrics](https://github.com/moehmeni/syncedlyrics) for lyrics synchronization
- [genanki](https://github.com/kerrickstaley/genanki) for Anki deck generation
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159) for Anki integration