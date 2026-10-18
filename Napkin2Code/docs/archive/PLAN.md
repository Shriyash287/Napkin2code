# Implementation contract

Default provider: Gemma 4 through the hosted Gemini API. Discover exact model IDs using the account's models.list() result and verify image support before saving selection. Never silently substitute a different model family.

Functions: `enhance(image_bytes) -> bytes`; `generate_text(prompt, system=None) -> str`; `generate_vision(prompt, image_bytes) -> str`; `sketch_to_spec(image_bytes) -> dict`; `extract_annotations(image_bytes) -> str`; `extract_html(text) -> str`; `spec_to_html(spec) -> str`; `edit_html(html, instruction) -> str`.

HTTP: GET /api/health; POST /api/discover; POST /api/analyze (image to spec); POST /api/generate (image or reviewed spec to spec/html); POST /api/edit (html plus image or instruction to html). All error payloads use {error: readable_message}. All Gemini requests happen on the backend.

Pages: / (landing), /projects, /scan, /review, /builder, /models, /settings, /docs, /about. The scan/review/builder flow shares browser-local project state. Generated code executes only in an opaque-origin sandboxed iframe with network restrictions. Download exports the generated HTML.
