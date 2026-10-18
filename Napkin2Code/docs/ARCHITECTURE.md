# Architecture

## Frontend

`frontend/templates/` holds the Jinja HTML pages. `base.html` provides the shared layout. Flask renders these pages using absolute paths resolved from the project location, so changing the terminal's working directory does not break resource lookup.

`frontend/static/` holds `app.js`, `style.css`, and the SVG assets. Their public URLs remain `/static/...`. Browser code handles camera capture, sketch upload, editing, previews, and browser-local projects. It sends requests to the same server's `/api/...` endpoints.

## Backend

`backend/app.py` owns Flask routes, upload limits, local request guards, error responses, and the temporary in-memory preview store. It serves templates and static assets from `frontend/` and input sketches from the root `samples/` directory.

`backend/config.py` resolves the project root, loads the root `.env`, creates the Google API client, discovers available instruction-tuned Gemma 4 models, and persists the verified selection in the root `.model.json`. Both private files are ignored by Git. All model requests originate here or through the engine; credentials never enter browser responses.

`backend/core/image_processing.py` validates and normalizes uploaded images. `backend/engine/vision_ai.py` interprets sketches and annotations. `backend/engine/codegen.py` generates and edits complete HTML. `backend/engine/llm.py` coordinates hosted API calls and bounded retries. `backend/engine/prompts.py` holds prompt text.

`backend/tools/` contains command-line maintenance tasks. Invoke them as Python modules from the project root so imports use the backend package. The root `test_pipeline.py` delegates to the live pipeline tool to retain the required validation command.

## Request flow

```text
Browser → Flask page route → frontend/templates + frontend/static
Browser → /api/analyze → image processing → vision engine → hosted Gemini API
Browser → /api/generate or /api/edit → generation engine → hosted Gemini API
Browser → /api/preview → temporary preview store → sandboxed iframe
```

The frontend and backend share `http://127.0.0.1:5000`, so browser storage and same-origin API requests retain their existing behavior. There is no server database or container dependency.

## Supporting directories

- `tests/`: mocked backend/API tests plus an isolated browser fixture and browser regression.
- `samples/`: source images for the UI and live pipeline.
- `output/`: generated live validation artifacts, ignored by Git.
- `design-references/`: original design exports, preserved byte-for-byte.
- `docs/archive/`: historical source documentation, reports, and original checksums.

Run the app with `python run.py` and backend checks with `python -m unittest discover -s tests -v`. Actual AI validation uses `python test_pipeline.py` and requires valid provider credentials.
