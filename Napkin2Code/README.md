# Napkin2Code

Turn a paper sketch into an editable HTML prototype. Flask serves the vanilla HTML, CSS, and JavaScript frontend on one local address. AI requests run on the backend through Google's hosted Gemini API using a discovered, image-verified Gemma 4 model.

## Project structure

```text
Napkin2Code/
├── frontend/
│   ├── templates/             Jinja HTML pages and shared layout
│   └── static/                Browser JavaScript, styles, and SVG assets
├── backend/
│   ├── app.py                 Flask pages, API routes, preview sandbox
│   ├── config.py              Private credentials, paths, model discovery
│   ├── core/                  Image validation and processing
│   ├── engine/                Model calls, prompts, generation and edits
│   ├── tools/                 Discovery, sample creation, live validation
│   └── requirements.txt       Backend dependencies
├── tests/                     Backend tests and optional browser regression
├── samples/                   Input sketches and annotations
├── design-references/         Supplied, unchanged design exports
├── docs/
│   ├── ARCHITECTURE.md        Responsibilities and request flow
│   ├── screenshots/           Existing application screenshots
│   ├── examples/              Previously generated demo
│   └── archive/               Original documentation and historical manifest
├── output/                    Generated validation results; ignored by Git
├── .env                       Private backend key; ignored by Git
├── .env.example               Configuration template
├── .model.json                Discovered model selection; ignored by Git
├── run.py                     Local server entry point
├── start.bat                  Double-click launcher on Windows
├── test_pipeline.py            Real AI validation entry point
├── requirements.txt           Includes backend dependencies
└── requirements-dev.txt       Optional browser test dependencies
```

## Run on Windows

Open PowerShell in this `Napkin2Code` folder:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The existing private `.env` was carried into this folder. Keep it. On a fresh checkout only, copy `.env.example` to `.env` and set `GEMINI_API_KEY` locally. Do not put the key in frontend code or source control.

```powershell
.\.venv\Scripts\python.exe run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). Use **AI setup → Test connection & discover model** to verify model access. The frontend opens without working AI credentials, but generation requires a valid key, internet access, and an available Gemma 4 model. A cached `.model.json` is not proof that the current key still has access.

After setup, you can also double-click `start.bat` to start the server.

The frontend uses Flask templates, so open it through the server rather than opening HTML files directly. One Flask process serves both folders; no separate frontend server or build step is required.

## Validation and maintenance

Run commands from this folder:

```powershell
# Backend/API tests; model responses are mocked.
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

# Discover and image-test actual available Gemma 4 models.
.\.venv\Scripts\python.exe -m backend.tools.discover_models

# Real AI pipeline; sends sample images to Google and writes to output/.
.\.venv\Scripts\python.exe test_pipeline.py

# Recreate sample input images if needed.
.\.venv\Scripts\python.exe -m backend.tools.create_samples
```

The reorganization passed 41 backend/integration tests and a real sample AI pipeline. See [the current validation report](docs/VALIDATION.md) for results and testing limits.

For optional browser regression, install `requirements-dev.txt`, run the app on port 5000, run `python tests/browser_fixture_server.py` on port 5001, and run `python tests/browser_regression.py`. The fixture returns simulated AI responses. Its missing-key checks expect the real app to have no configured key; use an isolated test configuration rather than replacing your private `.env`.

## Data and design

Projects remain in browser local storage. Continue using the same hostname and port to retain access to those projects. Export a backup in Settings before clearing site data or changing browsers.

The interface uses frosted glass panels, translucent controls, and layered backgrounds while retaining the Warm Studio layout and indigo palette. Theme materials are defined in `frontend/static/glass.css`; component layout remains in `frontend/static/style.css`. AI requests send submitted images and prompts to Google. Credentials remain in the backend; this is hosted AI processing, not local inference. Generated previews run in a sandboxed iframe.

The material in `docs/archive/` describes the original flat layout and its historical test results. Use this README and `docs/ARCHITECTURE.md` for the current layout. The archived checksum manifest applies only to the original distribution.
