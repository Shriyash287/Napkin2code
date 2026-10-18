import json
import re
from backend.engine import prompts
from backend.engine.llm import generate_text
from backend.engine.vision_ai import validate_spec

def extract_html(text) -> str:
    start = re.search(r"<!doctype\s+html\s*>|<html(?:\s|>)", text, flags=re.I)
    end = list(re.finditer(r"</html\s*>", text, flags=re.I))
    if not start or not end or not re.search(r"<html(?:\s|>)", text, flags=re.I):
        raise RuntimeError("The model returned incomplete HTML. Please try generating again.")
    html = text[start.start():end[-1].end()]
    if len(html) > 1_000_000:
        raise RuntimeError("The generated page is too large. Try a smaller sketch.")
    return html

def spec_to_html(spec) -> str:
    validate_spec(spec)
    return extract_html(generate_text("Build this UI specification:\n" + json.dumps(spec), system=prompts.CODE_SYSTEM_PROMPT))

def edit_html(html, instruction) -> str:
    existing = extract_html(html)
    if not isinstance(instruction, str) or not instruction.strip():
        raise ValueError("Describe the change you want to make.")
    return extract_html(generate_text(prompts.EDIT_PROMPT + "\nEDIT REQUEST:\n" + instruction +
        "\nEXISTING HTML:\n" + existing, system=prompts.CODE_SYSTEM_PROMPT))
