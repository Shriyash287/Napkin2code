import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from PIL import Image
import config
from app import app, PREVIEWS
from core.image_processing import enhance
from engine.codegen import extract_html, spec_to_html, edit_html
from engine.vision_ai import parse_spec, sketch_to_spec, extract_annotations
from engine.llm import generate_text

SPEC = {"title":"Test login","elements":[{"type":"form","text":"Email, password, sign in"}]}
HTML = "<!doctype html><html><head><style>body{color:blue}</style></head><body><button>Sign in</button></body></html>"

def png(size=(90,60),mode="RGB"):
    b=io.BytesIO()
    Image.new(mode,size,"white").save(b,"PNG")
    return b.getvalue()

class ImageTests(unittest.TestCase):
    def test_normalizes_and_bounds(self):
        image=Image.open(io.BytesIO(enhance(png((1800,900)))))
        self.assertEqual(image.mode,"RGB")
        self.assertEqual(image.size,(1024,512))
        self.assertEqual(image.format,"JPEG")
    def test_transparency(self):
        self.assertEqual(Image.open(io.BytesIO(enhance(png(mode="RGBA")))).mode,"RGB")
    def test_corrupt_image(self):
        with self.assertRaises(ValueError): enhance(b"not an image")
    def test_oversize(self):
        with self.assertRaises(ValueError): enhance(b"x"*(10*1024*1024+1))
    def test_unsupported(self):
        data=io.BytesIO();Image.new("RGB",(10,10)).save(data,"GIF")
        with self.assertRaises(ValueError): enhance(data.getvalue())

class EngineTests(unittest.TestCase):
    def test_json_surrounding_prose_and_fences(self):
        self.assertEqual(parse_spec("Here is JSON:\n"+chr(96)*3+"json\n"+json.dumps(SPEC)+"\n"+chr(96)*3),SPEC)
    def test_invalid_spec(self):
        for value in ['{}','{"title":"x","elements":[]}','{"title":"x","elements":[1]}','nonsense']:
            with self.assertRaises(ValueError): parse_spec(value)
    @patch("engine.vision_ai.generate_vision",side_effect=["invalid",json.dumps(SPEC)])
    def test_json_retry(self,mock):
        self.assertEqual(sketch_to_spec(b"image"),SPEC)
        self.assertEqual(mock.call_count,2)
    @patch("engine.vision_ai.generate_vision",return_value="invalid")
    def test_json_retry_limit(self,mock):
        with self.assertRaises(RuntimeError):sketch_to_spec(b"image")
        self.assertEqual(mock.call_count,2)
    @patch("engine.vision_ai.generate_vision",return_value="NONE.")
    def test_annotations_none(self,_):
        self.assertEqual(extract_annotations(b"image"),"")
    def test_extract_html(self):
        self.assertEqual(extract_html("Here:\n"+chr(96)*3+"html\n"+HTML+"\n"+chr(96)*3),HTML)
    def test_rejects_partial_html(self):
        for value in ["<div>hello</div>","<html><body>cut off"]:
            with self.assertRaises(RuntimeError):extract_html(value)
    @patch("engine.codegen.generate_text",return_value=HTML)
    def test_generation_contract(self,mock):
        self.assertEqual(spec_to_html(SPEC),HTML)
        self.assertIn("Test login",mock.call_args.args[0])
    @patch("engine.codegen.generate_text",return_value=HTML)
    def test_edit_contract(self,mock):
        self.assertEqual(edit_html(HTML,"add a toggle"),HTML)
        self.assertIn("add a toggle",mock.call_args.args[0])
    @patch("config.api_key",return_value="")
    def test_missing_key(self,_):
        with self.assertRaisesRegex(RuntimeError,"GEMINI_API_KEY is missing"):generate_text("hello")
    @patch("engine.llm.time.sleep")
    @patch("config.ensure_model",return_value="models/gemma-4-26b-a4b-it")
    @patch("config.api_key",return_value="test-placeholder")
    @patch("config.client")
    def test_one_generation_retry(self,mock,*_):
        ai=mock.return_value.__enter__.return_value
        ai.models.generate_content.side_effect=[OSError("private detail"),SimpleNamespace(text="ok")]
        self.assertEqual(generate_text("hello",system="system"),"ok")
        self.assertEqual(ai.models.generate_content.call_count,2)
        self.assertEqual(ai.models.generate_content.call_args.kwargs["contents"],"system\n\nhello")
    def test_sanitized_provider_error(self):
        exc=SimpleNamespace(code=403,message="SECRET should not appear")
        self.assertNotIn("SECRET",config.safe_provider_error(exc))

class DiscoveryTests(unittest.TestCase):
    @patch("config.client")
    def test_prefers_smaller_discovered_model_and_probes_image(self,mock):
        models=[SimpleNamespace(name="models/gemma-4-31b-it",display_name="31b",supported_actions=["generateContent"]),
                SimpleNamespace(name="models/gemma-4-26b-a4b-it",display_name="26b",supported_actions=["generateContent"])]
        ai=mock.return_value.__enter__.return_value;ai.models.list.return_value=models
        ai.models.generate_content.return_value=SimpleNamespace(text="red")
        with tempfile.TemporaryDirectory() as folder,patch.object(config,"MODEL_FILE",Path(folder)/".model.json"):
            result=config.discover_model()
            self.assertEqual(result["name"],models[1].name)
            self.assertTrue(result["image_verified"])
            self.assertEqual(config.current_model(),models[1].name)
    @patch("config.client")
    def test_no_substitute(self,mock):
        mock.return_value.__enter__.return_value.models.list.return_value=[
            SimpleNamespace(name="models/gemini-test",supported_actions=["generateContent"])]
        with self.assertRaisesRegex(RuntimeError,"No instruction-tuned Gemma 4"):config.discover_model()

class ApiTests(unittest.TestCase):
    def setUp(self):
        app.testing=True
        self.client=app.test_client()
        self.headers={"X-Napkin-Request":"1"}
    def tearDown(self): app.testing=False
    def post(self,path,**kwargs):
        return self.client.post(path,headers=self.headers,**kwargs)
    def test_all_pages(self):
        for path in ["/","/projects","/scan","/review","/builder","/models","/settings","/docs","/about"]:
            with self.subTest(path=path):self.assertEqual(self.client.get(path).status_code,200)
    @patch("config.api_key",return_value="")
    def test_health_has_no_key(self,_):
        response=self.client.get("/api/health")
        self.assertFalse(response.json["configured"])
        self.assertNotIn("api_key",response.json)
        self.assertEqual(response.headers["Cache-Control"],"no-store")
    def test_cross_origin_blocked(self):
        r=self.client.post("/api/generate",headers={**self.headers,"Origin":"https://evil.example"},json={})
        self.assertEqual(r.status_code,403)
    def test_missing_guard_header(self):
        self.assertEqual(self.client.post("/api/generate",json={}).status_code,403)
    def test_foreign_host_blocked(self):
        self.assertEqual(self.client.get("/api/health",base_url="http://evil.example").status_code,403)
    def test_missing_image(self):
        self.assertEqual(self.post("/api/analyze",data={}).status_code,400)
    def test_invalid_image(self):
        r=self.post("/api/analyze",data={"image":(io.BytesIO(b"fake"),"bad.png")})
        self.assertEqual(r.status_code,400)
    def test_invalid_json_body(self):
        self.assertEqual(self.post("/api/generate",json=[]).status_code,400)
        self.assertEqual(self.post("/api/generate",json={"spec":{}}).status_code,400)
    @patch("app.sketch_to_spec",return_value=SPEC.copy())
    def test_analyze(self,_):
        r=self.post("/api/analyze",data={"image":(io.BytesIO(png()),"x.png"),"title":"Custom"})
        self.assertEqual(r.status_code,200);self.assertEqual(r.json["spec"]["title"],"Custom")
    @patch("app.spec_to_html",return_value=HTML)
    def test_generate_reviewed_spec(self,_):
        r=self.post("/api/generate",json={"spec":SPEC})
        self.assertEqual(r.status_code,200);self.assertEqual(r.json["html"],HTML)
    @patch("app.spec_to_html",return_value=HTML)
    @patch("app.sketch_to_spec",return_value=SPEC.copy())
    def test_generate_from_image(self,*_):
        r=self.post("/api/generate",data={"image":(io.BytesIO(png()),"x.png")})
        self.assertEqual(r.status_code,200)
    @patch("app.edit_html",return_value=HTML)
    def test_typed_edit(self,mock):
        self.assertEqual(self.post("/api/edit",json={"html":HTML,"instruction":"add dark mode"}).status_code,200)
        self.assertEqual(mock.call_args.args[1],"add dark mode")
    @patch("app.edit_html",return_value=HTML)
    @patch("app.extract_annotations",return_value="Add dark mode")
    def test_sketch_edit(self,vision,coder):
        r=self.post("/api/edit",data={"html":HTML,"image":(io.BytesIO(png()),"notes.png")})
        self.assertEqual(r.status_code,200);self.assertEqual(coder.call_args.args[1],"Add dark mode")
    @patch("app.extract_annotations",return_value="")
    def test_no_annotations(self,_):
        r=self.post("/api/edit",data={"html":HTML,"image":(io.BytesIO(png()),"notes.png")})
        self.assertEqual(r.status_code,400)
    @patch("app.spec_to_html",side_effect=RuntimeError("Safe model failure"))
    def test_safe_api_error(self,_):
        r=self.post("/api/generate",json={"spec":SPEC})
        self.assertEqual(r.status_code,503);self.assertEqual(r.json,{"error":"Safe model failure"})
    def test_preview_isolated(self):
        r=self.post("/api/preview",json={"html":HTML})
        self.assertEqual(r.status_code,200)
        preview=self.client.get(r.json["url"])
        self.assertIn("sandbox allow-scripts",preview.headers["Content-Security-Policy"])
        self.assertIn("connect-src 'none'",preview.headers["Content-Security-Policy"])
        self.assertNotIn("allow-same-origin",preview.headers["Content-Security-Policy"])
        self.assertEqual(preview.data.decode(),HTML)
    def test_preview_cache_bounded(self):
        PREVIEWS.clear()
        for _ in range(30):self.post("/api/preview",json={"html":HTML})
        self.assertEqual(len(PREVIEWS),24)
    def test_unknown_page(self):
        self.assertEqual(self.client.get("/missing").status_code,404)
    def test_no_stacktrace_on_unexpected_error(self):
        app.testing=False
        with patch("app.spec_to_html",side_effect=Exception("SECRET")):
            r=self.post("/api/generate",json={"spec":SPEC})
            self.assertEqual(r.status_code,500);self.assertNotIn(b"SECRET",r.data)

if __name__ == "__main__":
    unittest.main()
