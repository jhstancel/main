import re


def parse_mana_cost(mana_cost_str):
    """
    Parse a mana cost string like "{1}{W}{U}" into a dict with counts:
    Example:
      "{1}{W}{U}" -> {"C":1, "W":1, "U":1}
      "{2}{G}{G}" -> {"C":2, "G":2}
    For hybrid or phyrexian mana, treat them as 1 generic for simplicity.
    """
    # Remove whitespace
    mana_cost_str = mana_cost_str.strip()
    # Pattern to extract {X}
    pattern = r"\{([^}]*)\}"
    symbols = re.findall(pattern, mana_cost_str)
    mana_dict = {}
    for sym in symbols:
        # sym could be a number like "2" or a color like "W" or "U/B" for hybrid
        if sym.isdigit():
            # Generic mana
            add_to_dict(mana_dict, "C", int(sym))
        else:
            # For hybrid or phyrexian, just treat as 1 generic for simplicity
            # If it's a single color (W/U/B/R/G), count that color
            # If it's hybrid or phyrexian, count as generic
            if len(sym) == 1 and sym in ["W","U","B","R","G"]:
                add_to_dict(mana_dict, sym, 1)
            else:
                # Hybrid or other special symbol
                add_to_dict(mana_dict, "C", 1)
    return mana_dict


def add_to_dict(d, key, amt):
    if key not in d:
        d[key] = 0
    d[key] += amt
