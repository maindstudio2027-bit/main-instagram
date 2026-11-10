#!/usr/bin/env python3
"""Render a mAInd studio Instagram post (1080x1350) from a JSON spec.

Usage: python3 render_post.py spec.json out.png
spec keys: kind ("news"|"service"), kicker, headline (use *word* for azure highlight),
           body, cta, number (optional big decorative label, e.g. "01" or "AI")
"""
import json, sys, re, html, subprocess, tempfile, os

spec = json.load(open(sys.argv[1]))
out = os.path.abspath(sys.argv[2])

def hl(t):
    t = html.escape(t)
    return re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', t)

is_news = spec.get("kind") == "news"
tag = "AI NEL MONDO" if is_news else "mAInd STUDIO · SERVIZI"
deco = html.escape(spec.get("number", "AI" if is_news else "01"))

page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--ink:#0F1A26;--panel:#152333;--line:#28394D;--az:#7FB8E0;--chalk:#F1ECE2;--text:#ECF1F6;--muted:#A3B4C6}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;background:var(--ink);overflow:hidden}}
body{{font-family:'Inter',sans-serif;color:var(--text);position:relative}}
.grid{{position:absolute;right:0;top:0;width:540px;height:540px;background-image:linear-gradient(#1C2D40 2px,transparent 2px),linear-gradient(90deg,#1C2D40 2px,transparent 2px);background-size:90px 90px}}
.glow{{position:absolute;width:760px;height:760px;right:-300px;top:-300px;border-radius:50%;background:#152333;border:2px solid #28394D}}
.glow:after{{content:"";position:absolute;inset:150px;border-radius:50%;border:2px solid #7FB8E0;opacity:.5}}
.deco{{position:absolute;right:56px;bottom:250px;font-family:'Poppins';font-weight:700;font-size:420px;line-height:.8;color:transparent;-webkit-text-stroke:2px #2A4560;letter-spacing:-10px}}
.wrap{{position:absolute;inset:0;padding:84px 84px 72px;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.logo{{font-family:'Poppins';font-weight:700;font-size:46px;line-height:1;letter-spacing:-1px}}
.logo b{{color:var(--az)}}
.logo small{{display:block;font-size:15px;font-weight:500;letter-spacing:11px;margin-top:6px;color:var(--muted)}}
.tag{{font-size:22px;font-weight:600;letter-spacing:4px;color:var(--ink);background:var(--az);padding:14px 24px;border-radius:999px}}
.kicker{{margin-top:auto;font-size:28px;font-weight:600;color:var(--az);letter-spacing:1px;text-transform:uppercase;margin-bottom:28px;display:flex;align-items:center;gap:18px}}
.kicker:before{{content:"";width:56px;height:3px;background:var(--az)}}
h1{{font-family:'Poppins';font-weight:700;font-size:{spec.get('size',92)}px;line-height:1.04;letter-spacing:-2.5px;color:#fff;max-width:930px}}
h1 .hl{{color:var(--az)}}
.body{{margin-top:36px;font-size:34px;line-height:1.42;color:var(--muted);max-width:860px}}
.foot{{margin-top:60px;padding-top:30px;border-top:2px solid var(--line);display:flex;justify-content:space-between;align-items:center;font-size:26px}}
.foot .cta{{color:var(--chalk);font-weight:600}}
.foot .url{{color:var(--az);font-weight:600}}
</style></head><body>
<div class="grid"></div><div class="glow"></div><div class="deco">{deco}</div>
<div class="wrap">
 <div class="top"><div class="logo">m<b>AI</b>nd<small>STUDIO</small></div><div class="tag">{tag}</div></div>
 <div class="kicker">{html.escape(spec['kicker'])}</div>
 <h1>{hl(spec['headline'])}</h1>
 <div class="body">{hl(spec['body'])}</div>
 <div class="foot"><span class="cta">{html.escape(spec.get('cta','Scrivici in DM →'))}</span><span class="url">maindstudio.com</span></div>
</div></body></html>"""

d = tempfile.mkdtemp()
p = os.path.join(d, "post.html")
open(p, "w").write(page)
subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=1", "--window-size=1080,1350", f"--screenshot={out}", f"file://{p}"],
               check=True, capture_output=True)
print(out)
