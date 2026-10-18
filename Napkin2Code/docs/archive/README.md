# Napkin2Code

Turn a paper sketch into an editable HTML prototype. Built for the MLH Open Source AI Hackathon, with a minimal glassmorphism interface.

This implementation uses **Gemma 4 through Google's hosted Gemini API**, as specified in the supplied implementation brief. The website runs on your computer, but AI processing requires an API key and internet access. It is not an offline Ollama implementation; API availability, quotas and charges depend on your Google account.

![Scan workspace](docs/screenshots/scan-desktop.png)

## Included

- One navbar: Projects, Scan sketch, AI setup, Settings, How it works.
- Webcam capture, retake, image upload, drag-and-drop and a sample sketch.
- Editable interpretation outline and JSON before generation.
- Sandboxed interactive preview, HTML editor, detected specification, copy and download.
- Typed edits, annotated sketch edits and Undo.
- Browser-local projects with search, archive/restore and JSON backup import/export.
- Flask backend, vanilla HTML/CSS/JavaScript frontend; no Node build or database.

## Start on Windows

Tested with Python 3.13. Open PowerShell in the extracted project folder:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

If you already have a `.env`, keep it instead of copying over it. Edit that file locally:

```dotenv
GEMINI_API_KEY=your_key_here
```

Get your key from [Google AI Studio](https://aistudio.google.com/apikey). Do not put the key in frontend code, screenshots, chat, Git or the ZIP you share.

```powershell
.\.venv\Scripts\python.exe app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). Go to **AI setup** and select **Test connection & discover model**. This lists models available to your key and verifies image input with a small generated test image before saving the exact model ID in the ignored `.model.json` file. Restart the server after changing an existing API key.

The UI and local project tools also open without a key; AI actions show a setup message until configured.

### macOS / Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env locally, then:
.venv/bin/python app.py
```

## Use it

1. Open **Scan sketch** and capture a photo, upload one, or use the sample.
2. Name the project and select **Analyze sketch**.
3. Review or change the detected elements, then generate the website.
4. Try the preview, edit code directly, or describe a change.
5. For a paper edit, add notes to the sketch and upload or capture it again from the builder.
6. Download the single HTML file. Use **Settings** to export a project backup.

Projects are saved in this browser's local storage, not a server database. Changing browser, hostname or port changes that storage location. Clearing site data removes saved projects; use backup export first.

## Models

| Role | Selection | License / model card |
|---|---|---|
| Vision: sketch and annotation interpretation | Available instruction-tuned Gemma 4 model, discovered and image-tested at runtime | Apache 2.0; [official Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4) |
| Code generation and editing | The same verified Gemma 4 model | Apache 2.0; [official Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4) |

Model discovery dynamically selects and image-tests instruction-tuned Gemma 4 models at runtime (e.g. `models/gemma-4-26b-a4b-it`). Discovery prefers smaller active parameter counts among available candidates and never silently selects another model family. The model weight license is separate from the hosted API's terms.

See [Gemma on the Gemini API](https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api) for provider documentation.

## Source layout

```text
app.py                     Flask pages, APIs, preview sandbox
config.py                  Backend credentials and model discovery
core/image_processing.py   Image normalization and enhancement
engine/                    Vision, prompts, code generation and editing
templates/                 All page templates
static/                    Shared CSS, JavaScript and SVG icons
samples/                   Example sketch and annotated edit image
tests/                     Unit/API tests and isolated browser QA fixture
test_pipeline.py           Real-model sample pipeline and timings
discover_models.py         Command-line model discovery
design-references/         Original unmodified Stitch exports
docs/screenshots/          Actual app screenshots
```

## Checks

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

38 backend tests passed. The separate browser regression passed 14 grouped checks, including responsive layouts at 390, 768 and 1440 pixels. AI responses in the browser fixture are simulated; the camera test uses a synthetic video feed. See [TEST_REPORT.md](TEST_REPORT.md).

For browser regression, install `requirements-dev.txt` and Google Chrome. Run the real app on port 5000, run `python tests/browser_fixture_server.py` in a second terminal on port 5001, and run `python tests/browser_regression.py` in a third terminal, using the virtual environment's Python for each. The current regression expects the real app to have no configured key when testing its missing-key error. Port 5001 is only the test fixture.

After configuring a real key, run:

```powershell
.\.venv\Scripts\python.exe discover_models.py
.\.venv\Scripts\python.exe test_pipeline.py
```

The live pipeline writes per-sample HTML, JSON and measured timings to `output/`. It creates `demo_backup.html` upon successful real generation.

## Data and limitations

The selected image, prompts and code involved in AI requests are sent to Google. Camera video remains in the browser until a captured image is submitted. The API key remains on the Python backend.

Generated HTML runs in a sandboxed iframe that blocks network requests and parent-page access. The downloadable HTML is intended as a prototype; it does not provide a production database, authentication or payments. Preview restrictions do not apply when you independently open or host the exported file.

The server binds to loopback and is intended for local development. Image inputs support JPG, PNG and WebP up to 10 MB, normalized to a maximum 1024-pixel dimension. Browser storage is finite; export backups if it fills.

## License

The new application source is MIT licensed; see [LICENSE](LICENSE). Third-party packages, model weights and supplied design assets retain their own terms.
