import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://os.openmathmodel.org/v1"
KEY_FILE = Path(__file__).resolve().parents[1] / ".env"


def platform_key() -> str:
    key = os.environ.get("OPENMATHOS_PLATFORM_KEY", "").strip()
    if not key and KEY_FILE.exists():
        for line in KEY_FILE.read_text().splitlines():
            if line.startswith("OPENMATHOS_PLATFORM_KEY="):
                key = line.partition("=")[2].strip()
                break
    if not key or key.startswith("nuc_ak_"):
        raise ValueError("Set an OpenMathOS platform key (nuc_oc_...) in interrupt-harness/.env")
    return key


def post(operation: str, body: dict) -> dict:
    request = Request(
        f"{BASE}/{operation}",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {platform_key()}",
                 "Content-Type": "application/json", "User-Agent": "interrupt-harness/0.1"},
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        try:
            message = json.load(error).get("error", f"HTTP {error.code}")
        except (ValueError, AttributeError):
            message = f"HTTP {error.code}"
        raise ValueError(f"OpenMathOS {operation}: {message}") from None
    except (URLError, TimeoutError):
        raise ValueError(f"OpenMathOS {operation}: outcome uncertain; check the project before retrying") from None
