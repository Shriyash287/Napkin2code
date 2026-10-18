# Project instructions

1. The default provider is Gemma 4 via the hosted Gemini API. Discover available model names; never invent availability or claim local inference.
2. Never print, commit or expose GEMINI_API_KEY. Keep .env ignored and all model calls on the backend.
3. Preserve the supplied Warm Studio Precision layout, palette and styling in design-references/.
4. Use Flask and vanilla browser code. No Docker or server database. Do not push without explicit authorization.
5. Run `python -m unittest discover -s tests -v` for backend changes and `python test_pipeline.py` for live AI validation when credentials exist. Distinguish mocked tests from real model runs.
