class Card:
    def __init__(self, name, mana_cost, card_type, subtypes, color_identity, rules_text, legalities):
        self.name = name
        self.mana_cost = mana_cost     # string like "{1}{W}"
        self.card_type = card_type     # e.g. "Creature"
        self.subtypes = subtypes       # list of strings
        self.color_identity = color_identity  # list of chars e.g. ['W', 'U']
        self.rules_text = rules_text
        self.legalities = legalities   # dict from Scryfall: {format: "legal"/"not_legal"/...}

    def __repr__(self):
        return f"<Card: {self.name}>"

class Deck:
    def __init__(self, cards=None):
        self.cards = cards if cards else []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def card_count(self):
        return len(self.cards)

class Player:
    def __init__(self, owned_cards, preferred_format):
        self.owned_cards = owned_cards
        self.preferred_format = preferred_format  # "standard" or "commander"
