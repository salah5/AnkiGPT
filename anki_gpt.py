import anki_utils
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def create_anki_context_file(deck_name, front_field="kanji", back_field="meaning"):
    
    anki_cards = anki_utils.create_anki_cards_from_deck(deck_name, front_field, back_field)
    if not anki_cards:
        print(f"No cards found in deck: {deck_name}")
        return

    # Create a filename based on the deck name
    filename = f"anki_context_files/{deck_name.replace('::', '_')}.txt"
    
    with open(filename, 'w') as file:
        file.write("Available Decks and Cards:\n\n")
        file.write(f"Deck: {deck_name}\n")
        file.write("Format: Front | Back | Interval | Due | Reps \n")
        print(f"Writing cards for deck: {deck_name}")
        for card in anki_cards:
            file.write(card.card_string + "\n")
        file.write("\n")


if __name__ == "__main__":
    deck_name = "JLPT::N3::JLPT N3 Kanji Deck"
    deck_name = "JLPT::N3::JLPT N3 Vocabulary^ Deck"
    deck_name = "JLPT::N3::JLPT N3 Grammar Deck"
    create_anki_context_file(deck_name, front_field='grammar', back_field='meaning')
