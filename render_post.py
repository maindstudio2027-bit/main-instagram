#!/usr/bin/env python3
# mAInd studio – Instagram post renderer (1080x1350). Uso: python3 render_post.py spec.json out.png
import json, sys, re, html, subprocess, tempfile, os
spec = json.load(open(sys.argv[1])); out = os.path.abspath(sys.argv[2])

THEMES = {  # ink=sfondo, line=griglia/bordi, az=accento, muted=testo secondario
 "blu":      dict(ink="#0F1A26", line="#28394D", az="#7FB8E0", muted="#A3B4C6"),
 "corallo":  dict(ink="#1F1214", line="#4A2A2E", az="#FF8A73", muted="#CBAAA5"),
 "salvia":   dict(ink="#0F1F1A", line="#29443A", az="#7FD1A8", muted="#A3C2B5"),
 "viola":    dict(ink="#17132A", line="#352D52", az="#B59BFF", muted="#B5ADCF"),
 "ambra":    dict(ink="#1C170D", line="#43381F", az="#F2C14E", muted="#C9BC9A"),
 "rosa":     dict(ink="#24121C", line="#4F2A3E", az="#F59AC0", muted="#CFA9BB"),
 "petrolio": dict(ink="#0B1E22", line="#21454C", az="#5ED3D9", muted="#9EC3C6"),
}
T = THEMES.get(spec.get("theme", "blu"), THEMES["blu"])

# ---------- volti illustrati (personaggi inventati, nessuna persona reale) ----------
PRESETS = {
 "chef":     dict(bg="#E8B04B", skin="#F1C9A5", shirt="#2E4A62", style="chef",  extra=("apron",), hair="#3A2A20", label="Ristoranti"),
 "beauty":   dict(bg="#D97C8B", skin="#C68B63", shirt="#F1ECE2", style="bun",   extra=("earring",), hair="#1F1512", label="Beauty"),
 "studio":   dict(bg="#7FB8E0", skin="#E9B892", shirt="#1E3A55", style="short", extra=("glasses",), hair="#5B4334", label="Studi"),
 "artigiano":dict(bg="#6FA88A", skin="#8D5A3C", shirt="#C9643C", style="curly", extra=("beard","apron"), hair="#15100D", label="Artigiani"),
 "barista":  dict(bg="#C9643C", skin="#E0AC85", shirt="#1B1B1B", style="short", extra=("apron",), hair="#22160F", label="Bar"),
 "hotel":    dict(bg="#9FB7D9", skin="#F3D2B8", shirt="#23395B", style="long",  extra=("earring",), hair="#8A5A2B", label="Hotel"),
 "negozio":  dict(bg="#F2C14E", skin="#A86B4A", shirt="#2F6B57", style="long",  extra=(), hair="#120C0A", label="Negozi"),
 "dj":       dict(bg="#B59BFF", skin="#D9A07A", shirt="#2A2A2A", style="short", extra=("headphones",), hair="#2B1D16", label="Locali"),
 "titolare": dict(bg="#7FD1A8", skin="#EBC3A0", shirt="#F1ECE2", style="short", extra=("glasses","beard"), hair="#8E8E8E", label="Titolari"),
 "staff":    dict(bg="#F59AC0", skin="#B97A55", shirt="#1E3A55", style="curly", extra=("earring",), hair="#2A1A12", label="Staff"),
}
def face(i, p):
    s=[f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="c{i}"><circle cx="100" cy="100" r="100"/></clipPath></defs><g clip-path="url(#c{i})">',
       f'<rect width="200" height="200" fill="{p["bg"]}"/><circle cx="150" cy="40" r="70" fill="#fff" opacity=".08"/>']
    sk, hc, st, ex = p["skin"], p["hair"], p["style"], p["extra"]
    if st=="long": s.append(f'<path d="M54 95 Q50 36 100 36 Q150 36 146 95 L152 168 L48 168Z" fill="{hc}"/>')
    s.append(f'<path d="M22 210 Q24 152 100 146 Q176 152 178 210Z" fill="{p["shirt"]}"/>')
    s.append(f'<path d="M86 132 L86 152 Q100 164 114 152 L114 132Z" fill="{sk}" style="filter:brightness(.88)"/>')
    s.append('<path d="M84 150 L100 172 L116 150" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3"/>')
    if "apron" in ex: s.append('<path d="M70 210 L70 168 Q100 176 130 168 L130 210Z" fill="#F1ECE2"/><path d="M70 168 L84 150 M130 168 L116 150" stroke="#F1ECE2" stroke-width="4"/>')
    s.append(f'<ellipse cx="62" cy="100" rx="7" ry="10" fill="{sk}"/><ellipse cx="138" cy="100" rx="7" ry="10" fill="{sk}"/><ellipse cx="100" cy="96" rx="38" ry="44" fill="{sk}"/>')
    if st=="short": s.append(f'<path d="M61 96 Q56 46 100 46 Q144 46 139 96 Q134 70 112 66 Q86 74 66 72 Q62 82 61 96Z" fill="{hc}"/>')
    elif st=="long": s.append(f'<path d="M62 100 Q56 48 100 48 Q144 48 138 100 Q132 70 100 64 Q78 70 62 100Z" fill="{hc}"/>')
    elif st=="bun": s.append(f'<circle cx="100" cy="44" r="17" fill="{hc}"/><path d="M62 94 Q58 52 100 52 Q142 52 138 94 Q130 66 100 66 Q70 66 62 94Z" fill="{hc}"/>')
    elif st=="chef":
        s.append(f'<path d="M64 86 Q66 60 100 60 Q134 60 136 86 Q120 74 100 74 Q80 74 64 86Z" fill="{hc}"/>')
        s.append('<rect x="66" y="40" width="68" height="30" rx="6" fill="#fff"/><circle cx="76" cy="34" r="18" fill="#fff"/><circle cx="100" cy="26" r="21" fill="#fff"/><circle cx="124" cy="34" r="18" fill="#fff"/><rect x="66" y="58" width="68" height="10" fill="#E6EDF3"/>')
    elif st=="curly":
        for (x,y,r) in [(66,80,14),(76,62,15),(94,52,16),(112,52,16),(128,62,15),(136,80,14),(62,98,10),(140,98,10)]:
            s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{hc}"/>')
    if "beard" in ex: s.append(f'<path d="M62 100 Q64 146 100 146 Q136 146 138 100 Q132 126 116 124 Q100 120 84 124 Q68 126 62 100Z" fill="{hc}"/>')
    s.append(f'<path d="M80 86 Q87 82 94 86 M106 86 Q113 82 120 86" stroke="{hc}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    s.append('<circle cx="87" cy="99" r="4" fill="#1B1B1B"/><circle cx="113" cy="99" r="4" fill="#1B1B1B"/>')
    s.append('<circle cx="80" cy="114" r="7" fill="#E07A6B" opacity=".25"/><circle cx="120" cy="114" r="7" fill="#E07A6B" opacity=".25"/>')
    s.append('<path d="M100 102 Q97 110 102 112" stroke="#000" stroke-opacity=".25" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    s.append('<path d="M88 120 Q100 131 112 120" stroke="#5A2A22" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    if "glasses" in ex: s.append('<g fill="none" stroke="#14202C" stroke-width="3"><circle cx="87" cy="99" r="11"/><circle cx="113" cy="99" r="11"/><path d="M98 99 L102 99 M76 97 L64 94 M124 97 L136 94"/></g>')
    if "earring" in ex: s.append('<circle cx="62" cy="112" r="3.5" fill="#F2C14E"/><circle cx="138" cy="112" r="3.5" fill="#F2C14E"/>')
    if "headphones" in ex: s.append('<path d="M56 100 Q56 38 100 38 Q144 38 144 100" fill="none" stroke="#14202C" stroke-width="8"/><rect x="48" y="88" width="18" height="30" rx="8" fill="#14202C"/><rect x="134" y="88" width="18" height="30" rx="8" fill="#14202C"/>')
    s.append('</g></svg>'); return "".join(s)
def people_html(lst):
    if not lst: return ""
    out=['<div class="people">']
    for i,item in enumerate(lst[:4]):
        key,label = (item if isinstance(item,(list,tuple)) else (item, None))
        p = PRESETS.get(key, PRESETS["titolare"])
        out.append(f'<div class="pp"><div class="av">{face(i,p)}</div><span>{html.escape(label or p["label"])}</span></div>')
    out.append('</div>'); return "".join(out)

def hl(t):
    t = html.escape(t); return re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', t)
is_news = spec.get("kind") == "news"
tag = "AI NEL MONDO" if is_news else "mAInd STUDIO · SERVIZI"
deco = html.escape(spec.get("number", "AI" if is_news else "01"))
n_people = len(spec.get("people") or [])
page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--ink:{T['ink']};--line:{T['line']};--az:{T['az']};--chalk:#F1ECE2;--text:#ECF1F6;--muted:{T['muted']}}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;background:var(--ink);overflow:hidden}}
body{{font-family:'Inter',sans-serif;color:var(--text);position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:90px 90px;opacity:.35;-webkit-mask-image:radial-gradient(ellipse at 85% 10%,#000 0%,transparent 65%)}}
.glow{{position:absolute;width:900px;height:900px;right:-380px;top:-380px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--az) 30%,transparent),transparent 65%)}}
.deco{{position:absolute;right:56px;bottom:250px;font-family:'Poppins';font-weight:700;font-size:420px;line-height:.8;color:transparent;-webkit-text-stroke:2px color-mix(in srgb,var(--az) 24%,transparent);letter-spacing:-10px}}
.people{{position:absolute;left:84px;right:84px;top:250px;display:flex;justify-content:{'space-between' if n_people>=3 else 'center'};gap:{0 if n_people>=3 else 60}px}}
.pp{{display:flex;flex-direction:column;align-items:center;gap:18px}}
.pp:nth-child(even){{margin-top:70px}}
.av{{width:200px;height:200px;border-radius:50%;box-shadow:0 0 0 6px var(--ink),0 0 0 8px color-mix(in srgb,var(--az) 50%,transparent),0 24px 50px rgba(0,0,0,.45)}}
.av svg{{width:200px;height:200px;display:block}}
.pp span{{font-size:22px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--chalk);background:color-mix(in srgb,var(--ink) 90%,transparent);border:1px solid var(--line);padding:8px 18px;border-radius:999px}}
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
<div class="glow"></div><div class="grid"></div><div class="deco">{deco}</div>
{people_html(spec.get('people'))}
<div class="wrap">
 <div class="top"><div class="logo">m<b>AI</b>nd<small>STUDIO</small></div><div class="tag">{tag}</div></div>
 <div class="kicker">{html.escape(spec['kicker'])}</div>
 <h1>{hl(spec['headline'])}</h1>
 <div class="body">{hl(spec['body'])}</div>
 <div class="foot"><span class="cta">{html.escape(spec.get('cta','Scrivici in DM →'))}</span><span class="url">maindstudio.com</span></div>
</div></body></html>"""
d = tempfile.mkdtemp(); p = os.path.join(d, "post.html"); open(p, "w").write(page)
subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--force-device-scale-factor=1","--window-size=1080,1350",f"--screenshot={out}",f"file://{p}"],check=True,capture_output=True)
print(out)
