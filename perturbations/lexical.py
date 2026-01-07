"""
Lexical perturbations: small rewordings that should not change meaning.
Kept intentionally simple and original (no external synonym libraries required).
"""

import re
from typing import List


_SYNONYM_MAP = {
    r"\bapply\b": "use",
    r"\bfinal\b": "resulting",
    r"\bwhat is\b": "compute",
    r"\bexplain\b": "describe",
    r"\bunless\b": "except if",
    r"\bover time\b": "eventually",
    r"\bcan\b": "is it possible to"
}


def synonym_swap(text: str) -> str:
    out = text
    for pattern, repl in _SYNONYM_MAP.items():
        out = re.sub(pattern, repl, out, flags=re.IGNORECASE)
    return out


def punctuation_shift(text: str) -> str:
    # Minor punctuation changes
    out = text.replace("?", " ?").replace(".", ". ").strip()
    out = re.sub(r"\s+", " ", out)
    return out


def lexical_perturbations(text: str) -> List[str]:
    variants = []
    variants.append(synonym_swap(text))
    variants.append(punctuation_shift(text))
    variants.append(punctuation_shift(synonym_swap(text)))
    # Ensure uniqueness while preserving order
    seen = set()
    uniq = []
    for v in variants:
        if v not in seen:
            uniq.append(v)
            seen.add(v)
    return uniq
