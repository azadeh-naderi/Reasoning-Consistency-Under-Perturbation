"""
Structural perturbations: change formatting or order without changing the task.
"""

from typing import List


def add_bullets(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if len(lines) == 1:
        return "- " + lines[0]
    return "\n".join([f"- {l}" for l in lines])


def prepend_instruction(text: str) -> str:
    return "Read carefully and answer succinctly.\n\n" + text


def structural_perturbations(text: str) -> List[str]:
    variants = []
    variants.append(prepend_instruction(text))
    variants.append(add_bullets(text))
    variants.append(prepend_instruction(add_bullets(text)))

    seen = set()
    uniq = []
    for v in variants:
        if v not in seen:
            uniq.append(v)
            seen.add(v)
    return uniq
