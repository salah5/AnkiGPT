import requests
import os

# Configure the AnkiConnect API URL
ANKI_CONNECT_URL = "http://localhost:8765"

# Add configuration validation
def check_ankiconnect_running():
    try:
        response = requests.get(ANKI_CONNECT_URL)
        return True
    except requests.exceptions.ConnectionError:
        print("Error: AnkiConnect is not running. Please ensure:")
        print("1. Anki is running")
        print("2. AnkiConnect add-on is installed (Add-on code: 2055492159)")
        print("3. Anki is accepting connections on port 8765")
        return False

class AnkiCard:
    def __init__(self, deck_name, front, back, interval, ease, due, reps):
        self.deck_name = deck_name
        self.front = front
        self.back = back
        self.interval = interval
        self.ease = ease
        self.due = due
        self.reps = reps

        self.card_string = (
            "----------------------------\n"
            f"Deck Name: {self.deck_name}\n"
            "Front:\n"
            f"{self.front}\n"
            "Back:\n"
            f"{self.back}\n"
            "Review Status:\n"
            f"Interval: {self.interval} days\n"
            f"Ease Factor: {self.ease / 1000:.2f}\n"
            f"Due Date: {self.due}\n"
            f"Total Repetitions: {self.reps}"
        )

        self.card_string_for_context = f"{self.front}|{self.interval}|{self.ease}|{self.due}|{self.reps}"

class AnkiDeck:
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.cards = []
        self._load_cards()
    
    def _load_cards(self):
        """Internal method to load all cards from the deck"""
        note_ids = self._get_notes_from_deck()
        if not note_ids:
            print(f"No cards found in deck: {self.deck_name}")
            return

        notes = self._get_note_info(note_ids)
        for note in notes:
            card_ids = note.get("cards", [])
            if not card_ids:
                continue

            cards_info = self._get_cards_info(card_ids)
            for card in cards_info:
                anki_card = self._create_anki_card(note, card)
                self.cards.append(anki_card)

    def _get_notes_from_deck(self):
        payload = {
            "action": "findNotes",
            "version": 6,
            "params": {
                "query": f"deck:\"{self.deck_name}\""
            }
        }
        try:
            response = requests.post(ANKI_CONNECT_URL, json=payload)
            response_data = response.json()
            return response_data.get("result", [])
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving notes: {e}")
            return []

    def _get_note_info(self, note_ids):
        payload = {
            "action": "notesInfo",
            "version": 6,
            "params": {
                "notes": note_ids
            }
        }
        try:
            response = requests.post(ANKI_CONNECT_URL, json=payload)
            response_data = response.json()
            return response_data.get("result", [])
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving note info: {e}")
            return []

    def _get_cards_info(self, card_ids):
        payload = {
            "action": "cardsInfo",
            "version": 6,
            "params": {
                "cards": card_ids
            }
        }
        try:
            response = requests.post(ANKI_CONNECT_URL, json=payload)
            response_data = response.json()
            return response_data.get("result", [])
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving card info: {e}")
            return []

    def _create_anki_card(self, note, card):
        fields = note.get("fields", {})
        deck_name = card['deckName']

        # Heuristic: Use the first field as the front, all others as the back
        field_items = list(fields.items())
        front = field_items[0][1]['value'] if field_items else ""
        back = "\n".join(f"{name}: {data['value']}" for name, data in field_items[1:] if data['value'])

        interval = card.get("interval", "Unknown")
        ease = card.get("factor", "Unknown")
        due = card.get("due", "Unknown")
        reps = card.get("reps", "Unknown")

        return AnkiCard(deck_name, front, back, interval, ease, due, reps)

    def display_cards(self):
        """Display all cards in the deck"""
        for card in self.cards:
            print(card.card_string)

    @staticmethod
    def get_all_deck_names():
        """Get names of all available decks"""
        payload = {
            "action": "deckNames",
            "version": 6
        }
        try:
            response = requests.post(ANKI_CONNECT_URL, json=payload)
            response_data = response.json()
            return response_data.get("result", [])
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving deck names: {e}")
            return []

    @staticmethod
    def display_all_deck_names():
        """Display names of all available decks"""
        decks = AnkiDeck.get_all_deck_names()
        if not decks:
            print("No decks available.")
            return
        print("Available Decks:")
        for idx, deck in enumerate(decks):
            print(f"{idx + 1}. {deck}")

    def create_context_file(self, output_directory="assets/anki_context_files"):
        """Create a context file containing all cards in the deck"""
        if not self.cards:
            print(f"No cards found in deck: {self.deck_name}")
            return

        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Create a filename based on the deck name
        filename = f"{output_directory}/{self.deck_name.replace('::', '_')}.txt"
        
        with open(filename, 'w') as file:
            file.write(f"Deck: {self.deck_name}\n")
            file.write("Format: \nFront|Interval|Ease|Due|Reps\n")
            print(f"Writing cards for deck: {self.deck_name}")
            for card in self.cards:
                file.write(card.card_string_for_context + "\n")
            file.write("\n")


if __name__ == "__main__":
    # decks = AnkiDeck.get_all_deck_names()
    decks = ["JLPT::N3::JLPT N3 Kanji Deck", "JLPT::N3::JLPT N3 Vocabulary Deck", "JLPT::N3::JLPT N3 Grammar Deck"]
    for deck in decks:
        deck = AnkiDeck(deck)
        deck.create_context_file()