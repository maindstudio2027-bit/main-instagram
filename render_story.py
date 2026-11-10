#!/usr/bin/env python3
# mAInd studio – Storia Instagram 1080x1920 a partire dalla grafica del post.
# Uso: python3 render_story.py post.png out.png [tema] [testo_sopra] [testo_sotto]
import sys, os, base64, subprocess, tempfile, html
post, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
theme = sys.argv[3] if len(sys.argv) > 3 else "blu"
top = sys.argv[4] if len(sys.argv) > 4 else "Nuovo post"
bottom = sys.argv[5] if len(sys.argv) > 5 else "Tocca il profilo per leggerlo tutto"
THEMES = {"blu":("#0F1A26","#28394D","#7FB8E0"),"corallo":("#1F1214","#4A2A2E","#FF8A73"),"salvia":("#0F1F1A","#29443A","#7FD1A8"),
          "viola":("#17132A","#352D52","#B59BFF"),"ambra":("#1C170D","#43381F","#F2C14E"),"rosa":("#24121C","#4F2A3E","#F59AC0"),
          "petrolio":("#0B1E22","#21454C","#5ED3D9")}
ink, line, az = THEMES.get(theme, THEMES["blu"])
img = base64.b64encode(open(post, "rb").read()).decode()
page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;background:{ink};overflow:hidden;font-family:'Inter',sans-serif;color:#ECF1F6}}
.grid{{position:absolute;inset:0;background-image:linear-gradient({line} 1px,transparent 1px),linear-gradient(90deg,{line} 1px,transparent 1px);background-size:90px 90px;opacity:.35}}
.wrap{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:56px;padding:0 64px}}
.top{{font-family:'Poppins';font-weight:700;font-size:64px;letter-spacing:-1.5px;text-align:center}}
.top b{{color:{az}}}
.card{{width:880px;border-radius:36px;overflow:hidden;box-shadow:0 0 0 4px {az},0 40px 90px rgba(0,0,0,.55)}}
.card img{{width:880px;display:block}}
.bot{{font-size:36px;font-weight:600;color:{ink};background:{az};padding:22px 40px;border-radius:999px;text-align:center}}
</style></head><body><div class="grid"></div><div class="wrap">
<div class="top">m<b>AI</b>nd · {html.escape(top)}</div>
<div class="card"><img src="data:image/png;base64,{img}"></div>
<div class="bot">{html.escape(bottom)} ↑</div></div></body></html>"""
d = tempfile.mkdtemp(); p = os.path.join(d, "story.html"); open(p, "w").write(page)
subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--force-device-scale-factor=1",
                "--window-size=1080,1920",f"--screenshot={out}",f"file://{p}"],check=True,capture_output=True)
print(out)
