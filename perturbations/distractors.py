"""
Distractor perturbations: add irrelevant context that should not affect the answer.
This is a common failure trigger for brittle reasoning.
"""

from typing import List


_DISTRACTORS = [
    "Context (irrelevant): The weather today is sunny and mild.",
    "Note (irrelevant): Some people prefer answers in metric units.",
    "Extra (irrelevant): This question appeared in a practice worksheet."
]


def add_prefix_distractor(text: str) -> str:
    return _DISTRACTORS[0] + "\n\n" + text


def add_suffix_distractor(text: str) -> str:
    return text + "\n\n" + _DISTRACTORS[1]


def add_both(text: str) -> str:
    return _DISTRACTORS[2] + "\n\n" + text + "\n\n" + _DISTRACTORS[1]


def distractor_perturbations(text: str) -> List[str]:
    variants = [add_prefix_distractor(text), add_suffix_distractor(text), add_both(text)]
    seen = set()
    uniq = []
    for v in variants:
        if v not in seen:
            uniq.append(v)
            seen.add(v)
    return uniq
