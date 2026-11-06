"""Bedienoberfläche für den Webseiten-Generator (lokal im Browser, nur auf diesem Rechner erreichbar).

  .venv/bin/python generator/gui.py        (oder Doppelklick auf Webseiten-Generator.command)

Link einfügen, optional Excel + Fotos wählen, Design und Farbkonzept wählen (oder eigenes Farbkonzept mit
Farbwählern anlegen), „Vorschau erstellen“ bzw. „Kundenauswahl erstellen“. Ergebnisse liegen in vorschau/."""
import base64
import json
import os
import re
import sys
import threading
import time
import traceback
import urllib.parse
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import designs  # noqa: E402
import erstelle_webseite as gen  # noqa: E402

PORT = 8765
SETTINGS = os.path.join(HERE, "einstellungen.json")          # nicht im Git (enthält den API-Schlüssel)
LOCK = threading.Lock()


def load_settings():
    try:
        return json.load(open(SETTINGS, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_settings(d):
    json.dump(d, open(SETTINGS, "w", encoding="utf-8"), indent=1)
    os.chmod(SETTINGS, 0o600)


def api_key():
    return os.environ.get("GOOGLE_MAPS_API_KEY") or load_settings().get("google_api_key", "")


def url_for(path):
    rel = os.path.relpath(path, os.path.join(ROOT, "vorschau"))
    return "/vorschau/" + urllib.parse.quote(rel.replace(os.sep, "/"))


PAGE = r"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Webseiten-Generator</title>
<style>
:root{--bg:#f6f4f1;--card:#fff;--line:#e3ddd5;--text:#26221e;--muted:#7a7068;--acc:#9a7a4a}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text)}
header{padding:18px 28px;border-bottom:1px solid var(--line);background:#fff;display:flex;justify-content:space-between;align-items:center}
header h1{font-size:19px;margin:0}header small{color:var(--muted)}
main{display:grid;grid-template-columns:minmax(420px,560px) 1fr;gap:22px;padding:22px 28px}
.box{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;margin-bottom:16px}
.box h2{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 12px}
label{display:block;font-size:13px;margin:10px 0 4px;color:var(--muted)}
input[type=text],input[type=password]{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:8px;font-size:14px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
.opt{border:2px solid var(--line);border-radius:10px;padding:10px;cursor:pointer;background:#fff}
.opt.sel{border-color:var(--acc);box-shadow:0 0 0 3px #9a7a4a22}
.opt b{font-size:13px;display:block}.opt span{font-size:11.5px;color:var(--muted);display:block;margin-top:2px;line-height:1.35}
.sw{display:flex;gap:3px;margin-top:6px}.sw i{width:18px;height:12px;border-radius:3px;border:1px solid #0002;display:inline-block}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
button{padding:11px 16px;border-radius:8px;border:1px solid var(--acc);background:var(--acc);color:#fff;font-size:14px;cursor:pointer}
button.sec{background:#fff;color:var(--acc)}button:disabled{opacity:.5;cursor:wait}
.pick{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.pick div{display:flex;flex-direction:column}.pick input[type=color]{width:100%;height:38px;border:1px solid var(--line);border-radius:8px;padding:2px;background:#fff}
details summary{cursor:pointer;font-size:13px;color:var(--muted);margin-top:10px}
.warn{font-size:12.5px;margin-top:8px}.warn .bad{color:#b3261e}.warn .ok{color:#2e7d32}
#mock{border-radius:10px;overflow:hidden;border:1px solid var(--line);margin-top:12px;font-size:12px}
#mock .n{display:flex;justify-content:space-between;padding:8px 12px}#mock .h{padding:18px 12px}
#mock .t{font-size:20px;font-family:Georgia,serif}#mock .t em{font-style:italic}
#mock .b{display:inline-block;margin-top:10px;padding:6px 12px;font-size:11px}#mock .c{margin:0 12px 12px;padding:10px;border-radius:6px}
#log{font:12px Menlo,monospace;white-space:pre-wrap;color:var(--muted);max-height:150px;overflow:auto}
.links a{display:inline-block;margin:4px 10px 4px 0;color:var(--acc);font-weight:600}
iframe{width:100%;height:78vh;border:1px solid var(--line);border-radius:12px;background:#fff}
.hint{font-size:12px;color:var(--muted);margin-top:6px}
</style></head><body>
<header><h1>✂️ Webseiten-Generator für Friseure</h1><small id="keyinfo"></small></header>
<main><div>
 <div class="box"><h2>1 · Salon</h2>
  <label>Google-Maps-Link</label><input type="text" id="link" placeholder="https://maps.app.goo.gl/…  oder  https://www.google.com/maps/place/…">
  <label>Excel mit Salon-Daten und Fotos (optional)</label><input type="file" id="files" multiple accept=".xlsx,image/*">
  <div class="hint">Excel-Vorlage: generator/salon_daten_vorlage.xlsx – Fotos mit denselben Dateinamen wie in der Excel mit auswählen.</div>
 </div>
 <div class="box"><h2>2 · Design</h2><div class="grid" id="designs"></div></div>
 <div class="box"><h2>3 · Farbkonzept</h2><div class="grid" id="farben"></div>
  <div class="box" id="eigen" style="margin:12px 0 0;display:none">
   <label>Name des Farbkonzepts</label><input type="text" id="ename" value="Mein Farbkonzept">
   <div class="pick" style="margin-top:8px">
    <div><label>Hintergrund</label><input type="color" id="c_bg" value="#fbf7f2"></div>
    <div><label>Text</label><input type="color" id="c_text" value="#2b2420"></div>
    <div><label>Akzent</label><input type="color" id="c_acc" value="#a0522d"></div>
   </div>
   <details><summary>Feinabstimmung (sonst automatisch)</summary><div class="pick">
    <div><label>Abschnitte</label><input type="color" id="c_black"></div>
    <div><label>Karten / Flächen</label><input type="color" id="c_mid"></div>
    <div><label>Text gedämpft</label><input type="color" id="c_muted"></div></div>
    <div class="hint">Wer hier etwas ändert, legt die Farbe fest; „automatisch“ setzt alles zurück.
     <a href="#" id="autoreset">automatisch</a></div></details>
   <div class="warn" id="warn"></div>
   <label style="margin-top:12px"><input type="checkbox" id="save" checked> Farbkonzept speichern (steht dann in der Liste)</label>
  </div>
  <div id="mock"><div class="n"><b>Salon</b><span>Home · Leistungen · Kontakt</span></div>
   <div class="h"><div class="t">Haare, die <em>für sich sprechen.</em></div><div>Ihr Friseur in Ihrer Stadt.</div>
   <span class="b">Termin buchen</span></div><div class="c">Karte: Damenschnitt · ab 45 €</div></div>
 </div>
 <div class="box"><h2>4 · Erstellen</h2>
  <div class="btns"><button id="go">Vorschau erstellen</button><button class="sec" id="goall">Kundenauswahl (alle Designs + Farben)</button></div>
  <div class="links" id="links"></div><div id="log"></div>
 </div>
 <div class="box"><h2>Einstellungen</h2>
  <label>Google-API-Schlüssel (Places API New) – bleibt nur auf diesem Rechner</label>
  <input type="password" id="key" placeholder="nicht gesetzt"><div class="btns"><button class="sec" id="savekey">Schlüssel speichern</button></div>
 </div>
</div>
<div><iframe id="view" src="about:blank"></iframe></div></main>
<script>
const $=id=>document.getElementById(id);let D={},design=null,farbe=null,manual={};
const lum=h=>{const c=[1,3,5].map(i=>parseInt(h.substr(i,2),16)/255).map(v=>v<=.03928?v/12.92:((v+.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2]};
const con=(a,b)=>{const[x,y]=[lum(a),lum(b)].sort((p,q)=>q-p);return (x+.05)/(y+.05)};
const mix=(a,b,t)=>'#'+[1,3,5].map(i=>Math.round(parseInt(a.substr(i,2),16)*(1-t)+parseInt(b.substr(i,2),16)*t).toString(16).padStart(2,'0')).join('');
function derive(){const bg=$('c_bg').value,tx=$('c_text').value,light=lum(bg)>.4;
 const auto={c_black:mix(bg,'#000000',light?.05:.30),c_mid:light?mix(bg,'#000000',.08):mix(bg,'#ffffff',.10),c_muted:mix(tx,bg,.42)};
 for(const k in auto) if(!manual[k]) $(k).value=auto[k];}
function custom(){return{name:$('ename').value||'Eigenes Farbkonzept',dark:$('c_bg').value,text:$('c_text').value,accent:$('c_acc').value,
 black:$('c_black').value,mid:$('c_mid').value,muted:$('c_muted').value}}
function pal(){return farbe==='eigen'?custom():D.farben.concat(D.eigene).find(f=>f.key===farbe)}
function paint(){const p=pal();if(!p)return;const m=$('mock');m.style.background=p.dark;m.style.color=p.text;
 m.querySelector('.n').style.background=p.black||p.dark;m.querySelector('.n').style.color=p.accent;
 m.querySelector('.t em').style.color=p.accent;const b=m.querySelector('.b');b.style.background=p.accent;b.style.color=p.dark;
 const c=m.querySelector('.c');c.style.background=p.mid;c.style.color=p.muted;
 if(farbe==='eigen'){const r1=con(p.text,p.dark),r2=con(p.accent,p.dark);
  $('warn').innerHTML=`Text/Hintergrund ${r1.toFixed(1)}:1 <span class="${r1>=4.5?'ok':'bad'}">${r1>=4.5?'✓ gut lesbar':'✗ zu wenig Kontrast (mind. 4,5)'}</span><br>`+
  `Akzent/Hintergrund ${r2.toFixed(1)}:1 <span class="${r2>=3?'ok':'bad'}">${r2>=3?'✓ Schaltflächen lesbar':'✗ Akzent zu ähnlich zum Hintergrund (mind. 3)'}</span>`;}}
function card(o,kind){const d=document.createElement('div');d.className='opt';d.dataset.key=o.key;
 const sw=o.dark?`<div class="sw">${[o.dark,o.mid,o.accent,o.text].map(c=>`<i style="background:${c}"></i>`).join('')}</div>`:'';
 d.innerHTML=`<b>${o.nr?o.nr+'. ':''}${o.name}</b><span>${o.text_de||''}</span>${o.head?`<span>${o.head} / ${o.body}</span>`:''}${sw}`;
 d.onclick=()=>select(kind,o.key);return d}
function select(kind,key){if(kind==='d'){design=key;document.querySelectorAll('#designs .opt').forEach(e=>e.classList.toggle('sel',e.dataset.key===key))}
 else{farbe=key;document.querySelectorAll('#farben .opt').forEach(e=>e.classList.toggle('sel',e.dataset.key===key));$('eigen').style.display=key==='eigen'?'block':'none';if(key==='eigen')derive();paint()}}
async function load(){D=await (await fetch('/api/daten')).json();
 $('designs').innerHTML='';D.designs.forEach(o=>$('designs').appendChild(card(o,'d')));
 $('farben').innerHTML='';D.farben.concat(D.eigene).forEach(o=>$('farben').appendChild(card(o,'f')));
 $('farben').appendChild(card({key:'eigen',name:'＋ Eigenes Farbkonzept',text_de:'Farben selbst auswählen'},'f'));
 $('keyinfo').textContent=D.api_key?'Google-Schlüssel gesetzt ✓':'Kein Google-Schlüssel – Daten nur aus Link-Name und Excel';
 select('d',design||D.designs[0].key);select('f',farbe||D.farben[0].key)}
['c_bg','c_text','c_acc'].forEach(k=>$(k).oninput=()=>{derive();paint()});
['c_black','c_mid','c_muted'].forEach(k=>$(k).oninput=()=>{manual[k]=1;paint()});
$('autoreset').onclick=e=>{e.preventDefault();manual={};derive();paint()};
async function upload(){const fs=[...$('files').files];if(!fs.length)return '';
 const files=await Promise.all(fs.map(f=>new Promise(r=>{const rd=new FileReader();rd.onload=()=>r({name:f.name,data:rd.result.split(',')[1]});rd.readAsDataURL(f)})));
 const res=await (await fetch('/api/upload',{method:'POST',body:JSON.stringify({files})})).json();return res.excel||''}
async function run(alle){$('go').disabled=$('goall').disabled=true;$('links').innerHTML='';
 $('log').textContent=alle?'Erstelle Kundenauswahl (10 Designs + 10 Farbkonzepte, ca. 1–2 Minuten) …':'Erstelle Vorschau …';
 try{const excel=await upload();const body={link:$('link').value.trim(),excel,design,alle};
  if(farbe==='eigen'){body.eigen=custom();body.speichern=$('save').checked}else body.farbe=farbe;
  const r=await (await fetch('/api/erstellen',{method:'POST',body:JSON.stringify(body)})).json();
  $('log').textContent=r.log||'';if(r.error){$('log').textContent+='\nFEHLER: '+r.error;return}
  let h=`<a href="${r.index}" target="_blank">Webseite öffnen</a><a href="${r.angebot}" target="_blank">Angebot (PDF)</a>`;
  if(r.auswahl)h+=`<a href="${r.auswahl}" target="_blank">Kundenauswahl</a><a href="${r.auswahl_pdf}" target="_blank">Kundenauswahl (PDF)</a>`;
  h+=`<div class="hint">Ordner: ${r.ordner}</div>`;$('links').innerHTML=h;$('view').src=r.auswahl||r.index;
  if(r.neu_farbe){farbe=r.neu_farbe;await load()}}
 catch(e){$('log').textContent+='\nFEHLER: '+e}finally{$('go').disabled=$('goall').disabled=false}}
$('go').onclick=()=>run(false);$('goall').onclick=()=>run(true);
$('savekey').onclick=async()=>{await fetch('/api/einstellungen',{method:'POST',body:JSON.stringify({google_api_key:$('key').value.trim()})});$('key').value='';load()};
load();
</script></body></html>"""


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):
        pass

    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            b = PAGE.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
        elif path == "/api/daten":
            self._json(dict(
                designs=[dict(nr=i, key=d["key"], name=d["name"], text_de=d["text_de"], head=d["head"], body=d["body"])
                         for i, d in enumerate(designs.DESIGNS, 1)],
                farben=[dict(nr=i, **{k: f[k] for k in ("key", "name", "text_de", "mode", "dark", "mid", "black",
                                                         "accent", "text", "muted")})
                        for i, f in enumerate(designs.FARBEN, 1)],
                eigene=designs.eigene_farben(), api_key=bool(api_key())))
        elif path.startswith("/vorschau/"):
            super().do_GET()                                   # Dateien aus vorschau/ (nur lesend)
        else:
            self.send_error(404)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        n = int(self.headers.get("Content-Length") or 0)
        data = json.loads(self.rfile.read(n) or b"{}")
        if path == "/api/upload":
            d = os.path.join(ROOT, "vorschau", "_upload", time.strftime("%Y%m%d-%H%M%S"))
            os.makedirs(d, exist_ok=True)
            excel = ""
            for f in data.get("files", []):
                name = os.path.basename(f["name"])
                with open(os.path.join(d, name), "wb") as fh:
                    fh.write(base64.b64decode(f["data"]))
                if name.lower().endswith(".xlsx"):
                    excel = os.path.join(d, name)
            self._json({"excel": excel})
        elif path == "/api/einstellungen":
            s = load_settings()
            s["google_api_key"] = data.get("google_api_key", "")
            save_settings(s)
            self._json({"ok": True})
        elif path == "/api/erstellen":
            lines = []
            try:
                with LOCK:
                    farbe, neu = data.get("farbe"), None
                    if data.get("eigen"):
                        e = data["eigen"]
                        farbe = designs.eigene_farbe(e["name"], e["dark"], e["text"], e["accent"],
                                                     e.get("black"), e.get("mid"), e.get("muted"))
                        if data.get("speichern"):
                            designs.speichere_eigene(farbe)
                            neu = farbe["key"]
                    res = gen.erstelle(data.get("link", ""), data.get("excel") or None, data.get("design"), farbe,
                                       bool(data.get("alle")), api_key=api_key(), log=lines.append)
                out = dict(index=url_for(res["index"]), angebot=url_for(res["angebot"]), ordner=res["out"],
                           log="\n".join(lines + [f"Fertig: {res['name']} – {res['design']}, {res['farbe']}"]),
                           neu_farbe=neu)
                if res.get("auswahl"):
                    out.update(auswahl=url_for(res["auswahl"]), auswahl_pdf=url_for(res["auswahl_pdf"]))
                self._json(out)
            except Exception as e:                              # Fehler in der Oberfläche anzeigen
                traceback.print_exc()
                self._json({"error": str(e), "log": "\n".join(lines)})
        else:
            self.send_error(404)


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}/"
    print(f"Webseiten-Generator läuft: {url}  (Beenden mit Ctrl+C)")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
