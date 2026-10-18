"""Local Flask server. API credentials never enter a template or browser response."""
import os
import re
import secrets
import threading
import time
from collections import OrderedDict
from flask import Flask, Response, jsonify, render_template, request, send_from_directory
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix
from backend import config
from backend.core.image_processing import enhance
from backend.engine.codegen import edit_html, extract_html, spec_to_html
from backend.engine.vision_ai import extract_annotations, sketch_to_spec, validate_spec

app = Flask(
    __name__,
    template_folder=str(config.FRONTEND_DIR / "templates"),
    static_folder=str(config.FRONTEND_DIR / "static"),
    static_url_path="/static",
)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
PREVIEWS = OrderedDict()
PREVIEW_LOCK = threading.Lock()
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024
app.config["MAX_FORM_MEMORY_SIZE"] = 2 * 1024 * 1024

@app.before_request
def local_api_guard():
    if request.path.startswith("/api/"):
        host = request.host.split(":")[0].lower()
        allowed = {"127.0.0.1", "localhost"}
        if os.getenv("VERCEL") or os.getenv("VERCEL_URL") or host.endswith(".vercel.app"):
            allowed.add(host)
        allowed_env = os.getenv("ALLOWED_HOSTS", "")
        if allowed_env:
            allowed.update(h.strip().lower() for h in allowed_env.split(",") if h.strip())
        if host not in allowed:
            return jsonify(error="Use the local Napkin2Code server address."), 403
        origin = request.headers.get("Origin")
        if origin:
            def _clean(u):
                return re.sub(r"^https?://", "", u.rstrip("/"))
            if _clean(origin) != _clean(request.host_url):
                return jsonify(error="This request must come from the Napkin2Code workspace."), 403
        if request.method == "POST" and request.headers.get("X-Napkin-Request") != "1":
            return jsonify(error="Please make this request from the Napkin2Code workspace."), 403

@app.after_request
def response_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Permissions-Policy"] = "camera=(self), microphone=()"

    if request.path.startswith("/preview/"):
        response.headers["Content-Security-Policy"] = "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; connect-src 'none'; frame-src 'none'; form-action 'none'; base-uri 'none'; sandbox allow-scripts"
        response.headers["Cache-Control"] = "no-store"
        return response
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data: blob:; font-src 'self'; media-src 'self' blob:; "
        "connect-src 'self'; frame-src 'self' blob:; object-src 'none'; base-uri 'none'")
    if request.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/")
def landing():
    return render_template("landing.html", page="home")

@app.get("/<page>")
def page_view(page):
    if page not in {"projects", "scan", "review", "builder", "models", "settings", "docs", "about"}:
        return render_template("not_found.html", page="404"), 404
    return render_template(page + ".html", page=page)

@app.get("/samples/<path:filename>")
def sample(filename):
    return send_from_directory(config.BASE_DIR / "samples", filename)

@app.get("/api/health")
def health():
    has_key, model = bool(config.api_key()), config.current_model()
    return jsonify(provider="gemini", configured=has_key, model=model,
        status="ready" if has_key and model else "needs_model" if has_key else "needs_key",
        message="Gemma 4 via Gemini API" if has_key and model else
        "Test the connection to discover an image-capable Gemma 4 model." if has_key else
        "Add GEMINI_API_KEY to your local .env file to enable AI generation.")

@app.post("/api/discover")
def discover():
    return jsonify(config.discover_model())

def image_input():
    upload = request.files.get("image")
    if upload is None:
        raise ValueError("Choose a sketch image first.")
    return enhance(upload.read())

def text_field(data, field, limit=4000):
    value = data.get(field, "")
    if not isinstance(value, str) or len(value) > limit:
        raise ValueError(f"{field.capitalize()} must be text shorter than {limit} characters.")
    return value.strip()

def apply_context(spec, data):
    title, instruction = text_field(data, "title", 200), text_field(data, "instruction")
    if title:
        spec["title"] = title
    if instruction:
        spec["instructions"] = instruction
    return spec

@app.post("/api/analyze")
def analyze():
    return jsonify(spec=apply_context(sketch_to_spec(image_input()), request.form))

@app.post("/api/generate")
def generate():
    if request.is_json:
        data = request.get_json()
        if not isinstance(data, dict):
            raise ValueError("Provide a JSON object containing a specification.")
        spec = validate_spec(data.get("spec"))
    else:
        spec = apply_context(sketch_to_spec(image_input()), request.form)
    return jsonify(spec=spec, html=spec_to_html(spec), model=config.current_model())

@app.post("/api/edit")
def edit():
    data = request.get_json() if request.is_json else request.form
    if not hasattr(data, "get"):
        raise ValueError("Provide the existing HTML and an editing instruction.")
    html = text_field(data, "html", 1_000_000)
    extract_html(html)
    instruction = text_field(data, "instruction")
    if "image" in request.files:
        instruction = "\n".join(part for part in [instruction, extract_annotations(image_input())] if part)
    if not instruction:
        raise ValueError("No edit annotations were found. Write a change on the sketch or type an instruction.")
    return jsonify(html=edit_html(html, instruction), instruction=instruction)


@app.post("/api/preview")
def create_preview():
    data = request.get_json()
    if not isinstance(data, dict):
        raise ValueError("Provide HTML to preview.")
    html = extract_html(text_field(data, "html", 1_000_000))
    token = secrets.token_urlsafe(24)
    with PREVIEW_LOCK:
        now = time.monotonic()
        for key in list(PREVIEWS):
            if now - PREVIEWS[key][0] > 1800:
                del PREVIEWS[key]
        while len(PREVIEWS) >= 24:
            PREVIEWS.popitem(last=False)
        PREVIEWS[token] = (now, html)
    return jsonify(url="/preview/" + token)

@app.get("/preview/<token>")
def preview(token):
    with PREVIEW_LOCK:
        entry = PREVIEWS.get(token)
    if entry is None or time.monotonic() - entry[0] > 1800:
        return Response("This preview expired. Reload the builder to create it again.", status=404, mimetype="text/plain")
    return Response(entry[1], mimetype="text/html")

@app.errorhandler(ValueError)
def bad_input(exc):
    return jsonify(error=str(exc)), 400

@app.errorhandler(RuntimeError)
def provider_failure(exc):
    return jsonify(error=str(exc)), 503

@app.errorhandler(HTTPException)
def http_failure(exc):
    messages = {400: "The request could not be read. Check the input and try again.",
        413: "This upload is too large. Choose an image smaller than 10 MB.",
        404: "This page or resource does not exist.", 405: "That request method is not supported."}
    if request.path.startswith("/api/"):
        return jsonify(error=messages.get(exc.code, "The request could not be completed.")), exc.code
    return render_template("not_found.html", page="404"), exc.code

@app.errorhandler(Exception)
def unexpected_failure(exc):
    if app.testing:
        raise exc
    return jsonify(error="The server could not finish this request. Please try again."), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
