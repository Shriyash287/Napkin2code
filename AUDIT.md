# Napkin2Code audit

## Inputs and initial state
Audited on 2026-10-18. The workspace was empty and was not a Git repository. The supplied Stitch package contains four static HTML mockups (landing, projects, camera scan, interpretation review), four screenshots, and Warm Studio Precision DESIGN.md. The repeated pasted briefs describe the same completion task. astra_master_prompt.txt adds complete navigation, audit tracking, and model-card verification requirements. No existing README, AGENTS, PLAN, Python code, sample images, or .env was supplied in the workspace.

## What works in the supplied design
The landing composition, shared sidebar/header, warm neutral/indigo palette, responsive grids, typography and panel styling exist. Camera state switching is simulated. Review view toggles, accordions, image rotation and contrast are local presentation interactions only. Nothing calls AI or persists projects.

## Stack and launch plan
Use Flask and vanilla HTML/CSS/JavaScript, preserving the supplied page layouts and design tokens. No Node build, Docker, server database or cloud deployment. Run `.venv/Scripts/python app.py` on Windows or `.venv/bin/python app.py` elsewhere. Browser stores projects locally. Gemini calls run on the Python backend only.

## Initial unfinished inventory
- [ ] Preserve supplied designs as reference files; adapt shared layout for mobile.
- [ ] Replace dead navigation, fake projects, fake statuses, hard-coded timings/confidence, account avatar and local-only claims.
- [ ] Implement backend config, key handling, model discovery and safe errors.
- [ ] Implement image normalization, sketch specification parsing and HTML generation/editing.
- [ ] Implement real webcam capture, retake, upload, drag-and-drop and sample sketch.
- [ ] Connect review outline/JSON to actual model results and editable specification.
- [ ] Add preview/code/spec builder, typed/sketch edits, Undo, copy and HTML download.
- [ ] Persist actual projects in browser storage with search/archive/open actions.
- [ ] Implement model/setup, settings, about and documentation navigation.
- [ ] Implement loading, missing-key, invalid-image, bad-model-output and camera errors.
- [ ] Test pipeline, backend and browser workflows, including responsive layouts.
- [ ] Save demo_backup.html only after a successful live AI generation.
- [ ] Document clean setup, hosted-data processing, models/license, limits and test results.
- [ ] Commit each completed phase locally, never push; check tracked files for secrets.

## Ordered implementation
1. Save this audit and unmodified design references; initialize local Git.
2. Create Flask API and the requested engine/core functions with runtime-discovered model selection.
3. Connect the four supplied layouts and add the matching builder/setup screens.
4. Run offline automated tests and browser checks. Run live model discovery and sample pipeline if credentials are available.
5. Update documentation and audit with actual outcomes and commit.

## Known initial blocker
GEMINI_API_KEY is absent from process environment and no workspace .env exists. Do not guess or claim a selected model. Live discovery, AI quality checks and an authentic generated demo backup depend on a key. Independent implementation and offline testing can continue.
