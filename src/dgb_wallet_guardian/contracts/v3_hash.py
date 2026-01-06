from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_sha256(payload: Dict[str, Any]) -> str:
    data = _canonical_json(payload).encode("utf-8")
    return hashlib.sha256(data).hexdigest()
