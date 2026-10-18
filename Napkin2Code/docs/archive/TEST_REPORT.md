# Validation report

Date: 2026-10-18. Environment: Windows, Python 3.13, Chrome through Playwright.

## Passed

- 38 backend unit/API tests: image validation and normalization, model discovery contracts, safe provider errors, specification parsing/retry, HTML validation, generation/edit endpoints, request-origin checks and preview restrictions.
- 14 browser check groups: five-link single navbar; sample loading; analysis/review/generation; interactive preview; typed and sketch edits; Undo; code/spec tabs; copy/download; reload persistence; project search/archive/restore; backup export/import; preview preference; camera capture/retake and upload; navigation; missing-key error/retry; responsive layouts; no uncaught JavaScript errors.
- Responsive checks covered eight pages at 390, 768 and 1440 pixels.
- Python compilation and JavaScript syntax checks.
- Visual review of actual scan page desktop and mobile screenshots.
- Live model discovery (`python discover_models.py`): Identified `models/gemma-4-26b-a4b-it` and `models/gemma-4-31b-it`; successfully verified image input probe with `models/gemma-4-26b-a4b-it`.
- Live AI test pipeline (`python test_pipeline.py`): Executed on `samples/login-sketch.png` with model `models/gemma-4-26b-a4b-it`. Image enhancement (0.051s), vision sketch-to-spec (87.451s), code generation spec-to-html (88.376s), total 175.885s. Output verified, valid UI specification and interactive login prototype produced, and `demo_backup.html` generated and saved.

The browser workflow used a separate port-5001 test server with deterministic mocked AI responses. Camera capture used Chrome's synthetic camera. These checks demonstrate application integration, while `test_pipeline.py` validated the real model output quality and live Gemma 4 vision/code generation on the Gemini API.

## Not verified

Physical webcam hardware compatibility (varies across client devices and user permissions). Real-time paper sketch iteration with handwritten red pen notes in physical conditions remains open for live user testing.

## Reproduction

Backend: `python -m unittest discover -s tests -v`.

Browser: install requirements-dev.txt and Chrome, start app.py on 5000 and tests/browser_fixture_server.py on 5001 in separate terminals, then run tests/browser_regression.py. Run with the real app unconfigured for its missing-key assertion. Results and screenshots are written to output/browser/.

Live AI: `python discover_models.py`, then `python test_pipeline.py`.

## Delivery

The source archive contains the application, tests, sample inputs, original design references, setup documentation and actual-app screenshots. It excludes credentials, selected-model cache, virtual environment, Git history and generated test outputs.
