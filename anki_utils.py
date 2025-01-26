import requests

# Configure the AnkiConnect API URL
ANKI_CONNECT_URL = "http://localhost:8765"

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
            f"Total Repetitions: {self.reps}\n"
        )


def get_notes_from_deck(deck_name):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f"deck:\"{deck_name}\""
        }
    }
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        response_data = response.json()
        return response_data.get("result", [])
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving notes: {e}")
        return []

def get_note_info(note_ids):
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

def get_cards_info(card_ids):
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

def create_anki_card(note, card):
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

def create_anki_cards_from_deck(deck_name):
    anki_cards = []
    note_ids = get_notes_from_deck(deck_name)
    if not note_ids:
        print(f"No cards found in deck: {deck_name}")
        return anki_cards

    notes = get_note_info(note_ids)
    for note in notes:
        card_ids = note.get("cards", [])
        if not card_ids:
            continue

        cards_info = get_cards_info(card_ids)
        for card in cards_info:
            anki_card = create_anki_card(note, card)
            anki_cards.append(anki_card)

    return anki_cards

def display_cards(deck_name):
    anki_cards = create_anki_cards_from_deck(deck_name)
    for anki_card in anki_cards:
        print(anki_card.card_string)

def get_deck_names():
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

def display_deck_names():
    decks = get_deck_names()
    if not decks:
        print("No decks available.")
        return
    print("Available Decks:")
    for idx, deck in enumerate(decks):
        print(f"{idx + 1}. {deck}")
