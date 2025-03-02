# AnkiGPT Project Guidelines

## Project Commands
- Run synced lyrics downloader: `python3 sync_lyrics.py`
- Create Anki deck from song: `python3 lyrics_to_anki.py "Song Name - Artist Name"`
- Generate context files: `python3 anki_utils.py`
- Install dependencies: `pip install -r requirements.txt`

## Environment Setup
- Requires Python 3.7+
- Anki with AnkiConnect add-on (code: 2055492159)
- `.env` file with API keys:
  ```
  DEEPSEEK_API_KEY=your_deepseek_api_key
  OPENAI_API_KEY=your_openai_api_key
  ```

## Code Style Guidelines
- Follow PEP 8 conventions
- Use descriptive variable names in snake_case
- Constants in UPPER_CASE at module top
- Document functions with docstrings
- Handle exceptions with specific error messages
- Use type hints for function parameters and returns
- Group related functionality in separate modules
- Path handling: use os.path.join() for cross-platform compatibility
- Directory structure: place assets in appropriate subfolders