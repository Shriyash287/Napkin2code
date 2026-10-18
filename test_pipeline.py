"""Live AI tests require a real API key; mock output is never substituted."""
import json
from pathlib import Path
from time import perf_counter
import config
from create_samples import create_samples
from core.image_processing import enhance
from engine.vision_ai import sketch_to_spec
from engine.codegen import spec_to_html

def main():
    root = Path(__file__).resolve().parent
    samples = root / "samples"
    if not any(p.suffix.lower() in {".png",".jpg",".jpeg",".webp"} for p in samples.glob("*")):
        create_samples()
    output = root / "output"
    output.mkdir(exist_ok=True)
    results = []
    for path in sorted(samples.iterdir()):
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        start = perf_counter()
        result = {"sample": path.name}
        try:
            image = enhance(path.read_bytes())
            image_end = perf_counter()
            spec = sketch_to_spec(image)
            vision_end = perf_counter()
            html = spec_to_html(spec)
            end = perf_counter()
            (output / (path.stem + ".html")).write_text(html, encoding="utf-8")
            (output / (path.stem + ".json")).write_text(json.dumps(spec, indent=2), encoding="utf-8")
            if not (root / "demo_backup.html").exists():
                (root / "demo_backup.html").write_text(html, encoding="utf-8")
            result.update(status="pass",model=config.current_model(),image_seconds=round(image_end-start,3),
                vision_seconds=round(vision_end-image_end,3),code_seconds=round(end-vision_end,3))
        except (RuntimeError, ValueError) as exc:
            result.update(status="blocked" if not config.api_key() else "fail",error=str(exc))
        result["total_seconds"] = round(perf_counter()-start,3)
        results.append(result)
        print(json.dumps(result))
    (output / "pipeline-results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 0 if results and all(r["status"] == "pass" for r in results) else 1

if __name__ == "__main__":
    raise SystemExit(main())
