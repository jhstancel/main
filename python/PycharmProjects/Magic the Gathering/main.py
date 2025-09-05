import sys
from deck_builder.data_fetcher import DataFetcher
from deck_builder.models import Player, Deck
from deck_builder.synergy_calculator import SynergyCalculator
from deck_builder.deck_optimizer import DeckOptimizer


def main():
    # Print format menu
    print("Select a format:")
    print("> commander (a)")
    print("> standard (b)")
    choice = input("Enter 'a' or 'b': ").strip().lower()

    if choice == 'a':
        game_format = "commander"
    elif choice == 'b':
        game_format = "standard"
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # Prompt for input mode
    print("Enter 'mass' to paste multiple card names at once, or just press Enter for normal input mode.")
    input_mode = input().strip().lower()

    owned_card_names = []
    if input_mode == 'mass':
        print("Please paste all your card names now. Press Enter on an empty line when done.")
        while True:
            line = input().strip()
            if line == "":
                break
            owned_card_names.append(line)
    else:
        print("Please enter the card names you own, one per line.")
        print("Press Enter on an empty line when done.")
        while True:
            line = input().strip()
            if line == "":
                break
            owned_card_names.append(line)

    print("Finished reading card names.")

    if not owned_card_names:
        print("No cards entered. Exiting.")
        sys.exit(0)

    # Initialize data fetcher and synergy calculator
    fetcher = DataFetcher()
    synergy_calc = SynergyCalculator()

    # Fetch the card data
    print("Fetching card data from Scryfall, please wait...")
    owned_cards = fetcher.fetch_cards(owned_card_names)

    # Create a Player object
    player = Player(owned_cards=owned_cards, preferred_format=game_format)

    # Initialize deck optimizer
    optimizer = DeckOptimizer(synergy_calc=synergy_calc, game_format=game_format)

    # Build the best deck
    print("Building the optimal deck...")
    best_deck = optimizer.build_optimal_deck(player)

    # Print the resulting deck
    print("\nOptimal Deck:")
    for card in best_deck.cards:
        print(f"- {card.name}")

    print(f"Deck Size: {best_deck.card_count()}")
    print("Deck building complete.")

    # Synergy query mode
    print("\nYou can now query synergy with a specific card in the deck.")
    print("Type 'synergy <card name>' to see top 5 synergistic cards and why.")
    print("Type 'done' to exit.")

    while True:
        command = input("> ").strip()
        if command.lower() == "done":
            break
        if command.lower().startswith("synergy "):
            query_card_name = command[8:].strip()
            query_card = None
            for c in best_deck.cards:
                if c.name.lower() == query_card_name.lower():
                    query_card = c
                    break
            if query_card is None:
                print("Card not found in deck.")
            else:
                # Compute synergy with all other cards
                other_cards = [x for x in best_deck.cards if x != query_card]
                scored_cards = []
                for oc in other_cards:
                    score, reasons = synergy_calc.compute_synergy_breakdown(query_card, oc)
                    scored_cards.append((oc, score, reasons))
                scored_cards.sort(key=lambda x: x[1], reverse=True)
                top_five = scored_cards[:5]

                print(f"Top synergy cards with {query_card.name}:")
                for i, (c, score, reasons) in enumerate(top_five, 1):
                    print(f"{i}. {c.name} (Score: {score:.2f})")
                    if reasons:
                        print("   Why:")
                        for r in reasons:
                            print(f"    - {r}")
                    else:
                        print("   No specific synergy reasons identified.")
        else:
            print("Unknown command. Type 'synergy <card name>' or 'done'.")

    print("Exiting synergy query mode. Goodbye!")


if __name__ == "__main__":
    main()
