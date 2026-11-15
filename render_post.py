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
# --- variazione dei volti: ogni giorno aspetto diverso (pelle, capelli, accessori, espressione, sfondo) ---
import random
_m = re.search(r"(\d{4})-(\d{2})-(\d{2})", os.path.basename(out))
SEED = int(spec.get("seed", int("".join(_m.groups())) if _m else 1))
SKINS = ["#F3D2B8","#EBC3A0","#E0AC85","#D9A07A","#C68B63","#B97A55","#A86B4A","#8D5A3C","#6E4530"]
HAIRS = ["#15100D","#2B1D16","#3A2A20","#5B4334","#8A5A2B","#B8742F","#D9B25F","#8E8E8E","#7A2E2E"]
SHIRTS= ["#2E4A62","#1E3A55","#2F6B57","#1B1B1B","#C9643C","#6247CF","#B8437A","#F1ECE2","#127A80","#9C6C06"]
BGS   = ["#E8B04B","#D97C8B","#7FB8E0","#6FA88A","#C9643C","#9FB7D9","#F2C14E","#B59BFF","#7FD1A8","#F59AC0","#5ED3D9","#FF8A73"]
FIXED = {  # elementi che identificano il ruolo
 "chef": dict(style="chef", extra={"apron"}), "barista": dict(extra={"apron"}), "artigiano": dict(extra={"apron"}),
 "dj": dict(extra={"headphones"}), "hotel": dict(extra={"bowtie"}), "beauty": dict(), "studio": dict(), "negozio": dict(),
 "titolare": dict(), "staff": dict(extra={"badge"}),
}
SHAPE = ["circle","squircle"][SEED % 2]
def vary(key, i):
    r = random.Random(SEED * 97 + i * 13 + sum(map(ord, key)))
    f = FIXED.get(key, {})
    style = f.get("style") or r.choice(["short","long","bun","curly","bald","ponytail","wavy","short","long"])
    extra = set(f.get("extra", set()))
    if r.random() < .22: extra.add("glasses")
    if style in ("short","curly","bald","wavy") and r.random() < .35: extra.add(r.choice(["beard","mustache"]))
    if style in ("long","bun","ponytail","wavy") and r.random() < .5: extra.add("earring")
    if key in ("artigiano","negozio") and style in ("short","bald") and r.random() < .4: extra.add("cap")
    used = set()
    bg = r.choice(BGS)
    return dict(bg=bg, skin=r.choice(SKINS), shirt=r.choice(SHIRTS), hair=r.choice(HAIRS[:7] if style!="bald" else HAIRS),
                style=style, extra=tuple(extra), mouth=r.choice(["smile","grin","soft"]), eyes=r.choice(["dot","dot","happy"]),
                label=PRESETS.get(key, PRESETS["titolare"])["label"])
def face(i, p):
    clip = '<circle cx="100" cy="100" r="100"/>' if SHAPE=="circle" else '<rect width="200" height="200" rx="56"/>'
    s=[f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="c{i}">{clip}</clipPath></defs><g clip-path="url(#c{i})">',
       f'<rect width="200" height="200" fill="{p["bg"]}"/><circle cx="150" cy="40" r="70" fill="#fff" opacity=".10"/><circle cx="30" cy="190" r="50" fill="#000" opacity=".06"/>']
    sk, hc, st, ex = p["skin"], p["hair"], p["style"], p["extra"]
    if st=="long": s.append(f'<path d="M54 95 Q50 36 100 36 Q150 36 146 95 L152 168 L48 168Z" fill="{hc}"/>')
    if st=="wavy": s.append(f'<path d="M56 96 Q48 40 100 38 Q152 40 144 96 Q150 120 140 140 Q130 128 136 110 L64 110 Q70 128 60 140 Q50 120 56 96Z" fill="{hc}"/>')
    if st=="ponytail": s.append(f'<path d="M132 70 Q170 80 160 140 Q150 120 138 100Z" fill="{hc}"/>')
    s.append(f'<path d="M22 210 Q24 152 100 146 Q176 152 178 210Z" fill="{p["shirt"]}"/>')
    s.append(f'<path d="M86 132 L86 152 Q100 164 114 152 L114 132Z" fill="{sk}" style="filter:brightness(.88)"/>')
    s.append('<path d="M84 150 L100 172 L116 150" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3"/>')
    if "apron" in ex: s.append('<path d="M70 210 L70 168 Q100 176 130 168 L130 210Z" fill="#F1ECE2"/><path d="M70 168 L84 150 M130 168 L116 150" stroke="#F1ECE2" stroke-width="4"/>')
    if "bowtie" in ex: s.append('<path d="M86 158 L100 165 L86 172Z M114 158 L100 165 L114 172Z" fill="#7A2E2E"/><circle cx="100" cy="165" r="4" fill="#7A2E2E"/>')
    if "badge" in ex: s.append('<rect x="122" y="172" width="30" height="20" rx="4" fill="#F1ECE2"/><rect x="127" y="178" width="20" height="3" fill="#888"/>')
    s.append(f'<ellipse cx="62" cy="100" rx="7" ry="10" fill="{sk}"/><ellipse cx="138" cy="100" rx="7" ry="10" fill="{sk}"/><ellipse cx="100" cy="96" rx="38" ry="44" fill="{sk}"/>')
    if st=="short": s.append(f'<path d="M61 96 Q56 46 100 46 Q144 46 139 96 Q134 70 112 66 Q86 74 66 72 Q62 82 61 96Z" fill="{hc}"/>')
    elif st in ("long","ponytail"): s.append(f'<path d="M62 100 Q56 48 100 48 Q144 48 138 100 Q132 70 100 64 Q78 70 62 100Z" fill="{hc}"/>')
    elif st=="wavy": s.append(f'<path d="M62 98 Q56 46 100 46 Q144 46 138 98 Q128 64 96 66 Q78 80 62 98Z" fill="{hc}"/>')
    elif st=="bun": s.append(f'<circle cx="100" cy="44" r="17" fill="{hc}"/><path d="M62 94 Q58 52 100 52 Q142 52 138 94 Q130 66 100 66 Q70 66 62 94Z" fill="{hc}"/>')
    elif st=="bald": s.append(f'<path d="M62 92 Q62 80 66 76 L66 96Z M138 92 Q138 80 134 76 L134 96Z" fill="{hc}"/><ellipse cx="88" cy="66" rx="12" ry="6" fill="#fff" opacity=".18"/>')
    elif st=="chef":
        s.append(f'<path d="M64 86 Q66 60 100 60 Q134 60 136 86 Q120 74 100 74 Q80 74 64 86Z" fill="{hc}"/>')
        s.append('<rect x="66" y="40" width="68" height="30" rx="6" fill="#fff"/><circle cx="76" cy="34" r="18" fill="#fff"/><circle cx="100" cy="26" r="21" fill="#fff"/><circle cx="124" cy="34" r="18" fill="#fff"/><rect x="66" y="58" width="68" height="10" fill="#E6EDF3"/>')
    elif st=="curly":
        for (x,y,r) in [(66,80,14),(76,62,15),(94,52,16),(112,52,16),(128,62,15),(136,80,14),(62,98,10),(140,98,10)]:
            s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{hc}"/>')
    if "cap" in ex: s.append(f'<path d="M60 78 Q62 44 100 44 Q138 44 140 78Z" fill="{p["shirt"]}"/><path d="M60 78 L156 78 Q150 88 100 84 Z" fill="{p["shirt"]}" style="filter:brightness(.8)"/>')
    if "beard" in ex: s.append(f'<path d="M62 100 Q64 146 100 146 Q136 146 138 100 Q132 126 116 124 Q100 120 84 124 Q68 126 62 100Z" fill="{hc}"/>')
    if "mustache" in ex: s.append(f'<path d="M84 116 Q92 110 100 114 Q108 110 116 116 Q108 120 100 117 Q92 120 84 116Z" fill="{hc}"/>')
    s.append(f'<path d="M80 86 Q87 82 94 86 M106 86 Q113 82 120 86" stroke="{hc if st!="bald" else "#3A2A20"}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    if p.get("eyes")=="happy": s.append('<path d="M82 101 Q87 95 92 101 M108 101 Q113 95 118 101" stroke="#1B1B1B" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    else: s.append('<circle cx="87" cy="99" r="4" fill="#1B1B1B"/><circle cx="113" cy="99" r="4" fill="#1B1B1B"/>')
    s.append('<circle cx="80" cy="114" r="7" fill="#E07A6B" opacity=".25"/><circle cx="120" cy="114" r="7" fill="#E07A6B" opacity=".25"/>')
    s.append('<path d="M100 102 Q97 110 102 112" stroke="#000" stroke-opacity=".25" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    m = p.get("mouth","smile")
    if m=="grin": s.append('<path d="M88 120 Q100 134 112 120Z" fill="#5A2A22"/><path d="M91 121 L109 121" stroke="#fff" stroke-width="3"/>')
    elif m=="soft": s.append('<path d="M92 122 Q100 128 108 122" stroke="#5A2A22" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    else: s.append('<path d="M88 120 Q100 131 112 120" stroke="#5A2A22" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    if "glasses" in ex: s.append('<g fill="none" stroke="#14202C" stroke-width="3"><circle cx="87" cy="99" r="11"/><circle cx="113" cy="99" r="11"/><path d="M98 99 L102 99 M76 97 L64 94 M124 97 L136 94"/></g>')
    if "earring" in ex: s.append('<circle cx="62" cy="112" r="3.5" fill="#F2C14E"/><circle cx="138" cy="112" r="3.5" fill="#F2C14E"/>')
    if "headphones" in ex: s.append('<path d="M56 100 Q56 38 100 38 Q144 38 144 100" fill="none" stroke="#14202C" stroke-width="8"/><rect x="48" y="88" width="18" height="30" rx="8" fill="#14202C"/><rect x="134" y="88" width="18" height="30" rx="8" fill="#14202C"/>')
    s.append('</g></svg>'); return "".join(s)
def people_html(lst):
    if not lst: return ""
    out=['<div class="people">']
    for i,item in enumerate(lst[:4]):
        key,label = (item if isinstance(item,(list,tuple)) else (item, None))
        p = vary(key if key in PRESETS else "titolare", i)
        out.append(f'<div class="pp"><div class="av">{face(i,p)}</div><span>{html.escape(label or p["label"])}</span></div>')
    out.append('</div>'); return "".join(out)

def hl(t):
    t = html.escape(t); return re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', t)
is_news = spec.get("kind") == "news"
tag = "AI NEL MONDO" if is_news else "mAInd STUDIO · SERVIZI"
deco = html.escape(spec.get("number", "AI" if is_news else "01"))
n_people = len(spec.get("people") or [])

# ---------- varianti: sfondo (bg) e impaginazione (layout) ----------
# bg: "scuro" (default) | "chiaro" (crema) | "pieno" (fondo pieno nel colore del tema)
# layout: "classico" (volti in alto) | "basso" (titolo in alto, volti in basso) | "centrato" | "card" (testo in un riquadro)
DARK_AZ = {"blu":"#2F6FA3","corallo":"#C9462E","salvia":"#2B7D58","viola":"#6247CF","ambra":"#9C6C06","rosa":"#B8437A","petrolio":"#127A80"}
bg_mode = spec.get("bg", "scuro"); layout = spec.get("layout", "classico")
tname = spec.get("theme", "blu")
if bg_mode == "chiaro":
    V = dict(bg="#F5F0E6", fg=T["ink"], az=DARK_AZ.get(tname,"#2F6FA3"), muted=f"color-mix(in srgb,{T['ink']} 68%,#F5F0E6)",
             line=f"color-mix(in srgb,{T['ink']} 14%,#F5F0E6)", pillbg="#FFFFFF", pillfg=T["ink"], tagbg=T["ink"], tagfg="#F5F0E6",
             hlbg="transparent", hlfg=DARK_AZ.get(tname,"#2F6FA3"), panel="#FFFFFF", glow=".10", shadow="rgba(0,0,0,.14)")
elif bg_mode == "pieno":
    V = dict(bg=T["az"], fg=T["ink"], az=T["ink"], muted=f"color-mix(in srgb,{T['ink']} 82%,{T['az']})",
             line=f"color-mix(in srgb,{T['ink']} 22%,{T['az']})", pillbg=T["ink"], pillfg=T["az"], tagbg=T["ink"], tagfg=T["az"],
             hlbg=T["ink"], hlfg=T["az"], panel=f"color-mix(in srgb,#fff 35%,{T['az']})", glow=".0", shadow="rgba(0,0,0,.22)")
else:
    bg_mode = "scuro"
    V = dict(bg=T["ink"], fg="#FFFFFF", az=T["az"], muted=T["muted"], line=T["line"], pillbg=f"color-mix(in srgb,{T['ink']} 90%,transparent)",
             pillfg="#F1ECE2", tagbg=T["az"], tagfg=T["ink"], hlbg="transparent", hlfg=T["az"],
             panel=f"color-mix(in srgb,{T['az']} 10%,{T['ink']})", glow=".30", shadow="rgba(0,0,0,.45)")
size = spec.get("size", 80)
if layout == "card": size = int(size * .9)
avs = 150 if layout in ("centrato",) else (170 if layout in ("basso","card") else 200)
center = layout == "centrato"

LAYOUT_CSS = {
 "classico": f".people{{margin-top:70px}} .txt{{margin-top:auto}} .deco{{right:56px;bottom:250px}}",
 "basso":    f".txt{{margin-top:80px;order:2}} .people{{order:3;margin-top:auto}} .foot{{order:4}} .pp:nth-child(even){{margin-top:40px}} .deco{{right:40px;bottom:330px;font-size:340px;opacity:.7}}",
 "centrato": f".people{{margin-top:70px;justify-content:center;gap:56px}} .pp:nth-child(even){{margin-top:0}} .txt{{margin-top:auto;text-align:center;display:flex;flex-direction:column;align-items:center}} .kicker{{justify-content:center}} .kicker:after{{content:'';width:56px;height:3px;background:var(--az)}} h1{{max-width:900px}} .body{{max-width:820px}} .deco{{left:50%;transform:translateX(-50%);bottom:300px;font-size:560px}}",
 "card":     f".people{{margin-top:60px}} .txt{{margin-top:auto;background:var(--panel);border:2px solid var(--line);border-radius:36px;padding:48px 52px 52px;box-shadow:0 30px 70px var(--shadow)}} .txt .body{{margin-top:26px;font-size:31px}} .deco{{display:none}} .foot{{margin-top:44px}}",
}
page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--bg:{V['bg']};--fg:{V['fg']};--line:{V['line']};--az:{V['az']};--muted:{V['muted']};--panel:{V['panel']};--shadow:{V['shadow']}}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;background:var(--bg);overflow:hidden}}
body{{font-family:'Inter',sans-serif;color:var(--fg);position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:90px 90px;opacity:.35;-webkit-mask-image:radial-gradient(ellipse at 85% 10%,#000 0%,transparent 65%)}}
.glow{{position:absolute;width:900px;height:900px;right:-380px;top:-380px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,{T['az']} 100%,transparent),transparent 65%);opacity:{V['glow']}}}
.deco{{position:absolute;font-family:'Poppins';font-weight:700;font-size:420px;line-height:.8;color:transparent;-webkit-text-stroke:2px color-mix(in srgb,var(--az) 24%,transparent);letter-spacing:-10px}}
.people{{display:flex;justify-content:{'space-between' if n_people>=3 and not center else 'center'};gap:{0 if n_people>=3 and not center else 60}px;padding:0 {0 if n_people>=3 else 0}px}}
.pp{{display:flex;flex-direction:column;align-items:center;gap:18px}}
.pp:nth-child(even){{margin-top:70px}}
.av{{width:{avs}px;height:{avs}px;border-radius:{'50%' if SHAPE=='circle' else '28%'};box-shadow:0 0 0 6px var(--bg),0 0 0 8px color-mix(in srgb,var(--az) 50%,transparent),0 24px 50px var(--shadow)}}
.av svg{{width:{avs}px;height:{avs}px;display:block}}
.pp span{{font-size:22px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{V['pillfg']};background:{V['pillbg']};border:1px solid var(--line);padding:8px 18px;border-radius:999px}}
.wrap{{position:absolute;inset:0;padding:84px 84px 72px;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:center;order:0}}
.people{{order:1}} .txt{{order:2}} .foot{{order:3}}
.logo{{font-family:'Poppins';font-weight:700;font-size:46px;line-height:1;letter-spacing:-1px;color:var(--fg)}}
.logo b{{color:var(--az)}}
.logo small{{display:block;font-size:15px;font-weight:500;letter-spacing:11px;margin-top:6px;color:var(--muted)}}
.tag{{font-size:22px;font-weight:600;letter-spacing:4px;color:{V['tagfg']};background:{V['tagbg']};padding:14px 24px;border-radius:999px}}
.kicker{{font-size:28px;font-weight:600;color:var(--az);letter-spacing:1px;text-transform:uppercase;margin-bottom:28px;display:flex;align-items:center;gap:18px}}
.kicker:before{{content:"";width:56px;height:3px;background:var(--az)}}
h1{{font-family:'Poppins';font-weight:700;font-size:{size}px;line-height:{1.16 if bg_mode=='pieno' else 1.06};letter-spacing:-2.5px;color:var(--fg);max-width:930px}}
.hl{{color:{V['hlfg']};background:{V['hlbg']};{'padding:0 .14em;border-radius:.12em;-webkit-box-decoration-break:clone;box-decoration-break:clone;' if bg_mode=='pieno' else ''}}}
.body .hl{{background:transparent;color:var(--fg);font-weight:600;padding:0}}
.body{{margin-top:36px;font-size:34px;line-height:1.42;color:var(--muted);max-width:860px}}
.foot{{margin-top:56px;padding-top:30px;border-top:2px solid var(--line);display:flex;justify-content:space-between;align-items:center;font-size:26px}}
.foot .cta{{color:var(--fg);font-weight:600}}
.foot .url{{color:var(--az);font-weight:600}}
{LAYOUT_CSS.get(layout, LAYOUT_CSS['classico'])}
</style></head><body>
<div class="glow"></div><div class="grid"></div><div class="deco">{deco}</div>
<div class="wrap">
 <div class="top"><div class="logo">m<b>AI</b>nd<small>STUDIO</small></div><div class="tag">{tag}</div></div>
 {people_html(spec.get('people'))}
 <div class="txt">
  <div class="kicker">{html.escape(spec['kicker'])}</div>
  <h1>{hl(spec['headline'])}</h1>
  <div class="body">{hl(spec['body'])}</div>
 </div>
 <div class="foot"><span class="cta">{html.escape(spec.get('cta','Scrivici in DM →'))}</span><span class="url">maindstudio.com</span></div>
</div></body></html>"""
d = tempfile.mkdtemp(); p = os.path.join(d, "post.html"); open(p, "w").write(page)
subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--force-device-scale-factor=1","--window-size=1080,1350",f"--screenshot={out}",f"file://{p}"],check=True,capture_output=True)
print(out)
