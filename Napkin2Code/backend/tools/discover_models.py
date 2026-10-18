from backend import config

if __name__ == "__main__":
    try:
        result = config.discover_model()
        print("Gemma models available to this account:")
        for name in result["available_gemma"]:
            print(" -", name)
        print("Selected image-verified model:", result["name"])
    except RuntimeError as exc:
        print("Discovery blocked:", str(exc))
        raise SystemExit(1)
