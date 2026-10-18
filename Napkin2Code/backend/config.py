"""Backend-only configuration. Credentials never belong in responses or logs."""
import json
import os
import re
import threading
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent
BASE_DIR = BACKEND_DIR.parent
FRONTEND_DIR = BASE_DIR / "frontend"
PROVIDER = "gemini"
MODEL_FILE = BASE_DIR / ".model.json"
MODEL_LOCK = threading.Lock()
GEMINI_MODEL = None

def api_key():
    load_dotenv(BASE_DIR / ".env", override=True)
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if (key.startswith('"') and key.endswith('"')) or (key.startswith("'") and key.endswith("'")):
        key = key[1:-1].strip()
    if key.startswith("AQ.AQ."):
        key = key[3:]
    return key

def current_model():
    global GEMINI_MODEL
    try:
        saved = json.loads(MODEL_FILE.read_text(encoding="utf-8"))
        name = saved.get("name", "")
        if re.fullmatch(r"(?:models/)?gemma-4-[a-zA-Z0-9.-]+-it", name) and saved.get("image_verified"):
            GEMINI_MODEL = name
            return name
    except (OSError, ValueError, AttributeError):
        pass
    GEMINI_MODEL = None
    return None

def client():
    from google import genai
    from google.genai import types
    key = api_key()
    if not key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to the local .env file, then test the connection in AI setup.")
    return genai.Client(api_key=key, http_options=types.HttpOptions(timeout=120_000))

def safe_provider_error(exc):
    code = getattr(exc, "code", None)
    if code in (401, 403):
        return "Google rejected the API credentials or access. Check the server's GEMINI_API_KEY and model permissions."
    if code == 429:
        return "Google's API quota or rate limit was reached. Check your account quota and try again later."
    if code == 404:
        return "The selected model is unavailable. Run model discovery again in AI setup."
    if code == 400:
        return "Google could not process this request. Try a clearer image or shorter instructions."
    return "The Gemini API could not complete the request. Check your connection and try again."

def discover_model():
    """List account models, verify Gemma 4 IT image input, save the exact ID."""
    from google.genai import types
    from PIL import Image, ImageDraw
    with MODEL_LOCK:
        with client() as ai:
            try:
                listed = list(ai.models.list())
            except Exception as exc:
                raise RuntimeError(safe_provider_error(exc)) from None
            available = [m for m in listed if "gemma" in (m.name or "").lower()]
            candidates = [m for m in available
                if re.fullmatch(r"(?:models/)?gemma-4-[a-zA-Z0-9.-]+-it", m.name or "")
                and "generateContent" in (m.supported_actions or [])]
            def size(model):
                active = re.search(r"-a(\d+(?:\.\d+)?)b", model.name.lower())
                total = re.search(r"-(\d+(?:\.\d+)?)b", model.name.lower())
                return (float(active.group(1)) if active else float(total.group(1)) if total else 999, model.name)
            candidates.sort(key=size)
            if not candidates:
                raise RuntimeError("No instruction-tuned Gemma 4 model supporting generateContent is available to this API key. No substitute model was selected.")
            probe = Image.new("RGB", (64, 64), "white")
            ImageDraw.Draw(probe).rectangle((16, 16, 48, 48), fill="red")
            buf = BytesIO()
            probe.save(buf, "JPEG")
            for model in candidates:
                try:
                    response = ai.models.generate_content(model=model.name, contents=[
                        "Name the color of the central square in one word.",
                        types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")])
                    if not response.text or "red" not in response.text.lower():
                        continue
                except Exception as exc:
                    if getattr(exc, "code", None) in (401, 403, 429):
                        raise RuntimeError(safe_provider_error(exc)) from None
                    if getattr(exc, "code", None) not in (400, 404):
                        raise RuntimeError(safe_provider_error(exc)) from None
                    continue
                record = {"name": model.name, "display_name": model.display_name,
                          "image_verified": True, "available_gemma": [m.name for m in available]}
                try:
                    temporary = MODEL_FILE.with_suffix(".tmp")
                    temporary.write_text(json.dumps(record, indent=2), encoding="utf-8")
                    temporary.replace(MODEL_FILE)
                except OSError:
                    raise RuntimeError("Model verified, but its selection could not be saved. Check workspace write access.") from None
                return record
            raise RuntimeError("Available Gemma 4 models did not pass the image-input check. No model was selected.")

def ensure_model():
    return current_model() or discover_model()["name"]
