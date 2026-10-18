"""Start the local Napkin2Code workspace."""
import os
from backend.app import app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
