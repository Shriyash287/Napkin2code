"""WSGI and local entry point for Napkin2Code."""
import os
from backend.app import app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
