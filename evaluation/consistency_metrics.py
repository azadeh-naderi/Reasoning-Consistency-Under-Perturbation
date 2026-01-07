"""
Consistency metrics:
- Exact match stability on normalized answers
- Numeric closeness for float answers (tolerance)
- Aggregate stability score across perturbations
"""

from typing import Any, List, Optional


def normalize_answer(x: Any) -> Any:
    if isinstance(x, str):
        return x.strip().lower()
    return x


def exact_match(a: Any, b: Any) -> bool:
    return normalize_answer(a) == normalize_answer(b)


def numeric_close(a: Any, b: Any, tol: float = 1e-3) -> Optional[bool]:
    try:
        af = float(a)
        bf = float(b)
        return abs(af - bf) <= tol
    except Exception:
        return None


def stability_score(final_answers: List[Any], reference: Any = None) -> float:
    """
    Stability score in [0,1].
    If reference is provided: proportion matching reference.
    Else: proportion matching the most common answer.
    """
    if not final_answers:
        return 0.0

    normalized = [normalize_answer(x) for x in final_answers]

    if reference is not None:
        ref_n = normalize_answer(reference)
        return sum(1 for x in normalized if x == ref_n) / len(normalized)

    # majority stability
    counts = {}
    for x in normalized:
        counts[x] = counts.get(x, 0) + 1
    max_count = max(counts.values())
    return max_count / len(normalized)
