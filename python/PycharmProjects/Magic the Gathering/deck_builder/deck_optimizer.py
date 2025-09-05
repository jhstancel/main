import math
from copy import deepcopy
from deck_builder.models import Deck
from deck_builder.utils import parse_mana_cost


class DeckOptimizer:
    def __init__(self, synergy_calc, game_format):
        self.synergy_calc = synergy_calc
        self.game_format = game_format
        # For demonstration, we define deck sizes:
        self.deck_size = 60 if game_format == "standard" else 100

    def build_optimal_deck(self, player):
        # 1. Filter by format legality
        valid_cards = self._filter_by_format(player.owned_cards, self.game_format)

        if len(valid_cards) < self.deck_size:
            # If not enough cards are valid, just return them all
            return Deck(cards=valid_cards)

        # 2. Attempt a synergy-based selection:
        #    We'll start by picking a "seed" card (the card with the best average synergy potential).
        #    Then iteratively add cards that increase synergy until we reach the deck size.

        seed_card = self._choose_seed_card(valid_cards)
        if not seed_card:
            # Fallback: just pick top deck_size cards by a simple heuristic
            return Deck(cards=valid_cards[:self.deck_size])

        deck = [seed_card]
        remaining_pool = [c for c in valid_cards if c != seed_card]

        # Iteratively add cards that yield the best synergy improvement
        while len(deck) < self.deck_size and len(remaining_pool) > 0:
            best_card, best_increase = None, -math.inf
            current_synergy = self.synergy_calc.compute_deck_synergy(deck)

            for c in remaining_pool:
                test_deck = deck + [c]
                new_synergy = self.synergy_calc.compute_deck_synergy(test_deck)
                synergy_increase = new_synergy - current_synergy

                # Also factor in mana curve balance:
                # We'll penalize adding cards that skew the curve too much.
                # Simple approach: prefer a balanced curve (2-3-4 mana)
                curve_penalty = self._curve_penalty(test_deck)
                final_score = synergy_increase - curve_penalty

                if final_score > best_increase:
                    best_increase = final_score
                    best_card = c

            if best_card:
                deck.append(best_card)
                remaining_pool.remove(best_card)
            else:
                # No improvement found, fill up with random
                break

        # If deck isn't full yet, just fill with random remaining cards
        if len(deck) < self.deck_size:
            deck += remaining_pool[:(self.deck_size - len(deck))]

        return Deck(cards=deck)

    def _choose_seed_card(self, cards):
        # Pick the seed card as the one that has the highest average synergy potential
        # i.e. sum synergy with all others / (count of others)
        if not cards:
            return None

        best_card = None
        best_score = -math.inf

        for card in cards:
            synergy_sum = 0.0
            for other in cards:
                if other != card:
                    synergy_sum += self.synergy_calc.compute_synergy_score(card, other)
            avg_synergy = synergy_sum / (len(cards) - 1) if len(cards) > 1 else 0
            if avg_synergy > best_score:
                best_score = avg_synergy
                best_card = card

        return best_card

    def _filter_by_format(self, cards, game_format):
        filtered = []
        for c in cards:
            if c.legalities.get(game_format, "not_legal") == "legal":
                filtered.append(c)
        return filtered

    def _curve_penalty(self, cards):
        # Simple mana curve check:
        # We'll parse mana costs and see distribution.
        # Ideal distribution: curve centered around 2-3-4 mana.
        cmc_list = []
        for c in cards:
            cmc = self._compute_cmc(c.mana_cost)
            cmc_list.append(cmc)
        if not cmc_list:
            return 0

        avg_cmc = sum(cmc_list) / len(cmc_list)
        # Penalize decks that move away from ~3.0 average CMC
        penalty = abs(avg_cmc - 3.0) * 0.5
        return penalty

    def _compute_cmc(self, mana_cost_str):
        mana = parse_mana_cost(mana_cost_str)
        # cmc is sum of all values in the mana dict
        return sum(mana.values())
