class SynergyCalculator:
    def __init__(self):
        pass

    def compute_synergy_score(self, card_a, card_b):
        # Original synergy calculation (no breakdown)
        # This is kept for backwards compatibility if needed
        score, _ = self.compute_synergy_breakdown(card_a, card_b)
        return score

    def compute_synergy_breakdown(self, card_a, card_b):
        """
        Return a tuple (score, reasons) where reasons is a list of human-readable strings
        explaining why the synergy score was assigned.
        """
        score = 0.0
        reasons = []

        # 1. Shared creature subtypes if both are creatures
        if "Creature" in card_a.card_type and "Creature" in card_b.card_type:
            shared_subtypes = set(card_a.subtypes).intersection(set(card_b.subtypes))
            if shared_subtypes:
                count = len(shared_subtypes)
                score += 1.0 * count
                reasons.append(f"Shared creature subtype(s): {', '.join(shared_subtypes)}")

        # 2. Both mention "draw a card"
        if "draw a card" in card_a.rules_text.lower() and "draw a card" in card_b.rules_text.lower():
            score += 0.5
            reasons.append("Both cards provide card draw effects.")

        # 3. Overlapping color identities
        shared_colors = set(card_a.color_identity).intersection(set(card_b.color_identity))
        if shared_colors:
            ccount = len(shared_colors)
            score_increase = 0.2 * ccount
            score += score_increase
            reasons.append(f"Shared colors: {', '.join(shared_colors)}")

        # 4. Tribal reference synergy
        # If card_a's rules mention a subtype card_b has, or vice versa.
        a_refs_b = False
        b_refs_a = False
        for st in card_a.subtypes:
            if st.lower() in card_b.rules_text.lower():
                score += 0.5
                reasons.append(f"{card_a.name} references a subtype ({st}) found on {card_b.name}.")
                a_refs_b = True
        for st in card_b.subtypes:
            if st.lower() in card_a.rules_text.lower():
                score += 0.5
                if not b_refs_a:  # Avoid printing duplicate reason multiple times
                    reasons.append(f"{card_b.name} references a subtype ({st}) found on {card_a.name}.")
                    b_refs_a = True

        return (score, reasons)

    def compute_deck_synergy(self, cards):
        total_score = 0.0
        if len(cards) < 2:
            return total_score
        for i in range(len(cards)):
            for j in range(i + 1, len(cards)):
                total_score += self.compute_synergy_score(cards[i], cards[j])
        return total_score
