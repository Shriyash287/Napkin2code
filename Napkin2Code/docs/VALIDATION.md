# Reorganization validation

Validated on October 18, 2026, after separating the frontend and backend.

## Backend and integration tests

Command: `.venv\Scripts\python.exe -m unittest discover -s tests -v`

Result: **41 tests passed** in the new project's own virtual environment. Model responses in this suite are mocked. Tests cover API behavior, image processing, discovery logic, preview isolation, frontend static assets, sample images, resource resolution outside the project working directory, and blocking access to private backend files.

The first sandboxed test attempt encountered Windows temporary-directory permissions. Running outside the sandbox passed. No application changes were needed to resolve that environmental restriction.

Command: `.venv\Scripts\python.exe -m pip check`

Result: **No broken requirements found.**

## Local HTTP checks

The new server runs from this folder using `.venv\Scripts\python.exe run.py` at `http://127.0.0.1:5000`.

The following routes returned HTTP 200: `/`, `/scan`, `/builder`, `/models`, `/static/app.js`, `/static/style.css`, and `/samples/login-sketch.png`.

## Actual provider validation

The live pipeline was invoked with `python test_pipeline.py` from this project, using the already installed parent workspace Python environment while the new environment finished installing the same application dependencies. This run made real hosted Google API calls; it did not use mocked responses.

Result: **PASS** for `login-sketch.png` using `models/gemma-4-26b-a4b-it`.

| Stage | Seconds |
| --- | ---: |
| Image preparation | 0.059 |
| Sketch interpretation | 92.489 |
| HTML generation | 97.667 |
| Total | 190.249 |

Generated HTML, specification JSON, demo backup, and measured results are under the ignored `output/` directory. See `output/pipeline-results.json` for machine-readable results. The nested annotation image is not included by the existing top-level sample pipeline.

A separate model-list request using the new project's own virtual environment succeeded and returned `models/gemma-4-26b-a4b-it` and `models/gemma-4-31b-it`. The saved model was present in that list. This confirms current authentication and availability, without guaranteeing future account quota or access.

## Design preservation and limits

At the time of the reorganization, all 11 templates, all nine design-reference files, the stylesheet, and both SVG assets were byte-identical to the original Downloads copy. The JavaScript change updated the disconnected-server error message from `python app.py` to `python run.py`.

The complete browser regression and physical camera flow were not rerun for this folder reorganization. Historical browser reports remain under `docs/archive/` and are not new test results.

## Glass theme update

The subsequent requested glassmorphism theme is defined in `frontend/static/glass.css`, linked from the shared `base.html` layout. It adds translucent surfaces, backdrop blur, warm layered backgrounds, and consistent borders and shadows. The original design-reference files remain unchanged.

Headless Chrome checks passed for the home, scan, projects, AI setup, settings, and documentation pages at 1440, 768, and 390 pixels: 18 responsive page checks with no horizontal overflow or JavaScript errors. Navigation from the home CTA, sample loading, and reduced-motion styling also passed. Screenshots and the check results are saved in the ignored `output/glass-theme/` directory. No new live AI run was required for this stylesheet and shared-template change.
