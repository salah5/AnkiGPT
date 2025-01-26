import os
import sys
import pydub
import genanki
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants moved to top and properly formatted
MP3_DIRECTORY = "music"
AUDIO_CLIPS_DIRECTORY = "audio_clips"
ANKI_DECKS_DIRECTORY = "anki_decks"

# Load API keys from environment variables
API_KEYS = {
    "deepseek": os.getenv('DEEPSEEK_API_KEY'),
    "openai": os.getenv('OPENAI_API_KEY')
}

def load_lrc(lrc_path):
    try:
        with open(lrc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except FileNotFoundError as e:
        print(f"Error loading lrc file {lrc_path}: {e}")
        return []

def load_mp3(mp3_path):
    try:
        audio = pydub.AudioSegment.from_mp3(mp3_path)
        return audio
    except Exception as e:
        print(f"Error loading MP3 file {mp3_path}: {e}")
        return None

def conv_to_ms(timestamp):
    """Convert timestamp to milliseconds."""
    return (
        int(timestamp[:2]) * 60 * 1000 +  # minutes to ms
        int(timestamp[3:5]) * 1000 +      # seconds to ms
        int(timestamp[6:8]) * 10          # centiseconds to ms
    )

def split_song(song_name):
    """Split song into clips and save them."""
    song_path = os.path.join(MP3_DIRECTORY, song_name)
    song_clips_dir = os.path.join(AUDIO_CLIPS_DIRECTORY, os.path.basename(song_path))

    if os.path.exists(song_clips_dir):
        print(f"Skipping {song_clips_dir}. Folder already exists.")
        return os.listdir(song_clips_dir)
    
    os.makedirs(song_clips_dir, exist_ok=True)
    os.makedirs(AUDIO_CLIPS_DIRECTORY, exist_ok=True)

    song = load_mp3(song_path + ".mp3")
    song_lines = load_lrc(song_path + ".lrc")

    clip_paths = []
    for i in range(len(song_lines)-1):

        start = conv_to_ms(song_lines[i][1:8])
        end = conv_to_ms(song_lines[i+1][1:8])

        # Extract the audio segment
        clip = song[start:end]
        
        clip_filename = f"clip_{i+1}.mp3"
        clip_path = os.path.join(song_clips_dir, clip_filename)
    
        # Export the clip
        clip.export(clip_path, format="mp3")
        clip_paths.append(clip_path)
        print(f"Exported clip {i+1} to {clip_path}")

    return clip_paths

def send_message_to_deepseek_api(prompt):
    """Send message to DeepSeek API."""
    url = 'https://api.deepseek.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEYS["deepseek"]}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'user', 'content': prompt}]
    }
    
    response = requests.post(url, headers=headers, json=payload).json()
    return response.get('choices', [{}])[0].get('message', {}).get('content')

def send_message_to_openai_api(prompt):
    """Send message to OpenAI API."""
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEYS["openai"]}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'gpt-4o',
        'messages': [{'role': 'user', 'content': prompt}]
    }
    
    response = requests.post(url, headers=headers, json=payload).json()
    return response.get('choices', [{}])[0].get('message', {}).get('content')

def translate_lyrics(song_name):

    lrc_path = os.path.join(MP3_DIRECTORY, song_name + '.lrc')

    # Load the LRC file
    song_lines = load_lrc(lrc_path)
    song_name = os.path.basename(lrc_path).replace('.lrc', '')

    # Batch translation request
    translation_prompt = (
        "I want to use an .lrc file to create anki flashcards for each line of the song."
        "Therefore it is necessary that I translate each timestamped line to english."
        "It is crucial that the total number of line and their order is preserved."
        "Even if the translation is not perfect, it's fine as long as each timestamped line"
        "gets the correct translation and also please add no additional comments or backticks of your own."
        "The number of lines MUST remain the same before and after the translation! And make sure that each translations gets its own line"
        "Hint: You can ensure alignment by checking if each line contains the same timestamp twice!"
        f"Here is the .lrc file: {song_lines}"
        )

    # Get all translations at once
    translation_response = send_message_to_deepseek_api(translation_prompt)
    translations = translation_response.split('\n')

    # for line, translation in zip(song_lines, translations):
    #     print(f"{line} - {translation}")

    translations = [item[10:] for item in translations]
    song_lines = [item[10:] for item in song_lines]


    assert len(translations) == len(song_lines), f"Translation count mismatch. Expected {len(song_lines)} translations, got {len(translations)}"

    return song_lines, translations

def create_anki_deck(song_name, song_lines, translations, audio_clips):
    
    # Create Anki deck and model
    my_model = genanki.Model(
        1607392319,
        'Song Lyrics Model',
        fields=[
            {'name': 'Audio'},
            {'name': 'Text'},
            {'name': 'Translation'},
        ],
        templates = [
            {
                'name': 'Card 1',
                'qfmt': '<div style="text-align: center; font-size: 20px;">{{Audio}}<br>{{Text}}</div>',
                'afmt': '<div style="text-align: center; font-size: 20px;">{{FrontSide}}<hr id="answer">{{Translation}}</div>',
            },
        ]
        )
    
    my_deck = genanki.Deck(
        2059400111,
        f'Song Lyrics::{song_name}'
    )

    #print(song_lines)
    
    # Create cards using the translations
    for i in range(len(song_lines)-1):
        # Get audio clip path
        clip_filename = f"clip_{i+1}.mp3"
        clip_path = os.path.join(AUDIO_CLIPS_DIRECTORY, song_name, clip_filename)

        #print(clip_path)
        
        # Create Anki note
        my_note = genanki.Note(
            model=my_model,
            fields=[
                f'[sound:{clip_filename}]',  # Audio
                song_lines[i],               # Original text
                translations[i]              # Translation
            ])
        
        my_deck.add_note(my_note)
    
    # Save the deck
    os.makedirs(ANKI_DECKS_DIRECTORY, exist_ok=True)
    package = genanki.Package(my_deck)
    package.media_files = [os.path.join(AUDIO_CLIPS_DIRECTORY, song_name, f"clip_{i+1}.mp3") for i in range(len(song_lines)-1)]
    package.write_to_file(os.path.join(ANKI_DECKS_DIRECTORY, f'{song_name}.apkg'))
    print(f"Created Anki deck for {song_name}")


if __name__ == "__main__":
    SONG_NAMES = [
        "“Ma Meilleure Ennemie” - Stromae, Pomme",
        "Again - Yui",
        "Departure - Masatoshi Ono",
        "Kenia OS - Malas Decisiones",
        "Akuma no Ko - Ai Higuchi"
    ]

    for song_name in SONG_NAMES:
        # Define the path to the expected Anki deck file
        deck_filename = f"{song_name}.apkg"
        deck_path = os.path.join(ANKI_DECKS_DIRECTORY, deck_filename)
        
        # Check if the deck already exists
        if os.path.exists(deck_path):
            print(f"Deck for '{song_name}' already exists at '{deck_path}'. Skipping...")
            continue  # Skip to the next song

        # Proceed with processing if the deck does not exist
        clip_paths = split_song(song_name)
        song_lines, translations = translate_lyrics(song_name)
        create_anki_deck(song_name, song_lines, translations, clip_paths)