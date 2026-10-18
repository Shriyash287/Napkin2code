import json
from backend.engine import prompts
from backend.engine.llm import generate_vision

def validate_spec(spec):
    if not isinstance(spec, dict):
        raise ValueError("The specification must be a JSON object.")
    if not isinstance(spec.get("title"), str) or not spec["title"].strip() or len(spec["title"]) > 200:
        raise ValueError("The specification needs a title between 1 and 200 characters.")
    elements = spec.get("elements")
    if not isinstance(elements, list) or not 1 <= len(elements) <= 100:
        raise ValueError("The specification needs an elements array with 1 to 100 items.")
    if any(not isinstance(e, dict) or not isinstance(e.get("type"), str) or not e["type"].strip() for e in elements):
        raise ValueError("Every specification element needs a text type.")
    if len(json.dumps(spec)) > 100_000:
        raise ValueError("The specification is too large.")
    return spec

def parse_spec(text):
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("The model did not return a JSON object.")
    try:
        return validate_spec(json.loads(text[start:end + 1]))
    except json.JSONDecodeError:
        raise ValueError("The model returned invalid JSON.") from None

def sketch_to_spec(image_bytes) -> dict:
    for attempt in range(2):
        prompt = prompts.SPEC_PROMPT
        if attempt:
            prompt += "\nYour previous response was not valid. Return exactly the required JSON shape."
        text = generate_vision(prompt, image_bytes)
        try:
            return parse_spec(text)
        except ValueError:
            pass
    raise RuntimeError("The model could not interpret this sketch as valid JSON. Try a clearer image with readable labels.")

def extract_annotations(image_bytes) -> str:
    text = generate_vision(prompts.ANNOTATION_PROMPT, image_bytes).strip()
    return "" if text.strip(chr(96) + " \n.").upper() == "NONE" else text
