# Napkin2Code audit

## Inputs and initial state
Audited on 2026-10-18. The workspace was empty and was not a Git repository. The supplied Stitch package contains four static HTML mockups (landing, projects, camera scan, interpretation review), four screenshots, and Warm Studio Precision DESIGN.md. The repeated pasted briefs describe the same completion task. astra_master_prompt.txt adds complete navigation, audit tracking, and model-card verification requirements. No existing README, AGENTS, PLAN, Python code, sample images, or .env was supplied in the workspace.

## What works in the supplied design
The landing composition, shared sidebar/header, warm neutral/indigo palette, responsive grids, typography and panel styling exist. Camera state switching is simulated. Review view toggles, accordions, image rotation and contrast are local presentation interactions only. Nothing calls AI or persists projects.

## Stack and launch plan
Use Flask and vanilla HTML/CSS/JavaScript, preserving the supplied page layouts and design tokens. No Node build, Docker, server database or cloud deployment. Run `.venv/Scripts/python app.py` on Windows or `.venv/bin/python app.py` elsewhere. Browser stores projects locally. Gemini calls run on the Python backend only.

## Initial unfinished inventory
- [x] Preserve supplied designs as reference files; adapt shared layout for mobile.
- [x] Replace dead navigation, fake projects, fake statuses, hard-coded timings/confidence, account avatar and local-only claims.
- [x] Implement backend config, key handling, model discovery and safe errors.
- [x] Implement image normalization, sketch specification parsing and HTML generation/editing.
- [x] Implement real webcam capture, retake, upload, drag-and-drop and sample sketch.
- [x] Connect review outline/JSON to actual model results and editable specification.
- [x] Add preview/code/spec builder, typed/sketch edits, Undo, copy and HTML download.
- [x] Persist actual projects in browser storage with search/archive/open actions.
- [x] Implement model/setup, settings, about and documentation navigation.
- [x] Implement loading, missing-key, invalid-image, bad-model-output and camera errors.
- [x] Test pipeline, backend and browser workflows, including responsive layouts.
- [x] Save demo_backup.html after successful live AI generation: verified with models/gemma-4-26b-a4b-it.
- [x] Document clean setup, hosted-data processing, models/license, limits and test results.
- [x] Commit each completed phase locally, never push; check tracked files for secrets.

## Ordered implementation
1. Save this audit and unmodified design references; initialize local Git.
2. Create Flask API and the requested engine/core functions with runtime-discovered model selection.
3. Connect the four supplied layouts and add the matching builder/setup screens.
4. Run offline automated tests and browser checks. Run live model discovery and sample pipeline if credentials are available.
5. Update documentation and audit with actual outcomes and commit.

## Resolved blocker and live validation
GEMINI_API_KEY was configured in `.env`. Live discovery identified `models/gemma-4-26b-a4b-it` and `models/gemma-4-31b-it`, selecting and image-verifying `models/gemma-4-26b-a4b-it`. The live pipeline executed against `samples/login-sketch.png`, producing specification JSON, HTML output, and an authentic `demo_backup.html` without errors.

## Delivery outcome

The shared sidebar has been replaced by the user's requested single navbar: Projects, Scan sketch, AI setup, Settings and How it works. Content was simplified and translucent glass panels applied throughout. All application, offline-test, and live model-quality validation work is complete. 38 backend tests, 14 browser check groups, and the live AI sample pipeline passed; see TEST_REPORT.md. Genuine `demo_backup.html` generated from the live Gemma 4 vision and code-generation pipeline. README documents the hosted Gemini implementation and setup. No secrets or virtual environment are included in the source archive. No code was pushed.
