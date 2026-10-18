"""Isolated browser QA server. Never run this as the real application.
Every AI response below is a deterministic test fixture, not model output.
Start: python tests/browser_fixture_server.py
"""
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import app as web

SPEC={"title":"Browser QA login","elements":[{"type":"form","text":"Email, password, Sign in","layout":"centered card"}],
      "notes":["Browser test fixture: no AI request was made."]}
HTML="""<!doctype html><html><head><meta name="viewport" content="width=device-width"><style>
body{font:16px Arial;margin:0;background:#f3f0fa;color:#25202c;display:grid;place-items:center;min-height:100vh}
main{background:white;border-radius:20px;padding:40px;max-width:320px}input{display:block;margin:12px 0;padding:10px}
button{background:#4f46e5;color:white;border:0;border-radius:8px;padding:12px;cursor:pointer}
body.dark{background:#171320;color:#eee}body.dark main{background:#282132}
small{display:block;color:#777;font-size:10px;margin-top:20px}
</style></head><body><main><h1>Welcome back</h1><label>Email<input type="email" placeholder="you@example.com"></label>
<label>Password<input type="password"></label><button id="signin">Sign in</button><p id="result"></p>
<!--EDIT--><small>Browser test fixture. No AI generation.</small></main><script>
document.getElementById('signin').onclick=()=>document.getElementById('result').textContent='Prototype form works.';
</script></body></html>"""
EDITED=HTML.replace("<!--EDIT-->","""<button id="dark">Toggle dark mode</button><script>
document.getElementById('dark').onclick=()=>document.body.classList.toggle('dark');
</script>""")

if __name__=="__main__":
    print("BROWSER QA FIXTURE SERVER: AI calls are mocked. Port 5001 only.")
    with patch.object(web,"sketch_to_spec",side_effect=lambda _:SPEC.copy()), \
         patch.object(web,"spec_to_html",return_value=HTML), \
         patch.object(web,"edit_html",return_value=EDITED), \
         patch.object(web,"extract_annotations",return_value="Add dark mode"), \
         patch.object(web.config,"api_key",return_value="test-only-placeholder"), \
         patch.object(web.config,"current_model",return_value="TEST FIXTURE - no AI"):
        web.app.run(host="127.0.0.1",port=5001,debug=False)
