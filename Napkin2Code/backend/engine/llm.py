import time
from google.genai import types
from backend import config

def _generate(contents):
    if not config.api_key():
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to the local .env file, then test the connection in AI setup.")
    model = config.ensure_model()
    with config.client() as ai:
        for attempt in range(2):
            try:
                result = ai.models.generate_content(model=model, contents=contents)
                if not result.text or not result.text.strip():
                    raise RuntimeError("The model returned no usable text. Try again with a clearer sketch.")
                return result.text.strip()
            except RuntimeError:
                if attempt:
                    raise
            except Exception as exc:
                if attempt or getattr(exc, "code", None) in (400, 401, 403, 404, 429):
                    raise RuntimeError(config.safe_provider_error(exc)) from None
            time.sleep(0.5)
    raise RuntimeError("The model returned no usable output.")

def generate_text(prompt, system=None) -> str:
    return _generate((system + "\n\n" if system else "") + prompt)

def generate_vision(prompt, image_bytes) -> str:
    return _generate([prompt, types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")])
