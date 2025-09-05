import requests
from deck_builder.models import Card

class DataFetcher:
    BASE_URL = "https://api.scryfall.com"

    def fetch_cards(self, card_names):
        cards = []
        for name in card_names:
            card_data = self._fetch_single_card(name)
            if card_data:
                card_obj = self._create_card_object(card_data)
                if card_obj:
                    cards.append(card_obj)
        return cards

    def _fetch_single_card(self, name):
        url = f"{self.BASE_URL}/cards/named?fuzzy={name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Warning: Could not find card '{name}'.")
            return None

    def _create_card_object(self, data):
        name = data['name']
        mana_cost = data.get('mana_cost', "")
        card_type_line = data.get('type_line', "")
        color_identity = data.get('color_identity', [])
        rules_text = data.get('oracle_text', "") or ""
        legalities = data.get('legalities', {})

        # Parse type line
        # Example: "Creature — Elf Druid"
        parts = card_type_line.split("—")
        main_type = parts[0].strip() if len(parts) > 0 else ""
        subtypes = []
        if len(parts) > 1:
            subtypes = [t.strip() for t in parts[1].split()]

        return Card(name, mana_cost, main_type, subtypes, color_identity, rules_text, legalities)
