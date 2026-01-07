"""
Parse model outputs into a standard schema.
We request JSON; this parser extracts it safely.
"""

import json
import re
from typing import Any, Dict

_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def extract_json(raw_text: str) -> Dict[str, Any]:
    raw_text = (raw_text or "").strip()

    try:
        return json.loads(raw_text)
    except Exception:
        pass

    m = _JSON_RE.search(raw_text)
    if not m:
        return {"final_answer": None, "rationale": None, "verification": None, "parse_error": "no_json_found"}

    try:
        return json.loads(m.group(0))
    except Exception as e:
        return {"final_answer": None, "rationale": None, "verification": None, "parse_error": f"json_decode_error: {e}"}
