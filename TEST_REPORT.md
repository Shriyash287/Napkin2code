# Validation report

Date: 2026-10-18. Environment: Windows, Python 3.13, Chrome through Playwright.

## Passed

- 38 backend unit/API tests: image validation and normalization, model discovery contracts, safe provider errors, specification parsing/retry, HTML validation, generation/edit endpoints, request-origin checks and preview restrictions.
- 14 browser check groups: five-link single navbar; sample loading; analysis/review/generation; interactive preview; typed and sketch edits; Undo; code/spec tabs; copy/download; reload persistence; project search/archive/restore; backup export/import; preview preference; camera capture/retake and upload; navigation; missing-key error/retry; responsive layouts; no uncaught JavaScript errors.
- Responsive checks covered eight pages at 390, 768 and 1440 pixels.
- Python compilation and JavaScript syntax checks.
- Visual review of actual scan page desktop and mobile screenshots.

The browser workflow used a separate port-5001 test server with deterministic mocked AI responses. Camera capture used Chrome's synthetic camera. These checks demonstrate application integration, not model output quality or physical webcam compatibility. The actual application is on port 5000.

## Not verified

No GEMINI_API_KEY was available. A real sample pipeline attempt returned a clear missing-key error after 0.125 seconds. Model availability for the user's account, live model selection, image interpretation quality, generated site quality, model latency and real AI edits remain unverified. No fabricated model timings or generated demo backup are included.

Next steps: configure the key, run discovery and test_pipeline.py, then visually check the real generated output and a real-camera capture.

## Reproduction

Backend: `python -m unittest discover -s tests -v`.

Browser: install requirements-dev.txt and Chrome, start app.py on 5000 and tests/browser_fixture_server.py on 5001 in separate terminals, then run tests/browser_regression.py. Run with the real app unconfigured for its missing-key assertion. Results and screenshots are written to output/browser/.

Live AI: `python discover_models.py`, then `python test_pipeline.py`.

## Delivery

The source archive contains the application, tests, sample inputs, original design references, setup documentation and actual-app screenshots. It excludes credentials, selected-model cache, virtual environment, Git history and generated test outputs.
