#!/usr/bin/env python3
"""Assemble <deck>/slides/sNN.html fragments into <deck>/deck.html, and render per-slide screenshots.

The deck root defaults to the current directory; override with --root DIR or DECK_ROOT.
Expected layout under the root: slides/sNN.html, assets/deck.css, build/ (previews), shots/ (PNGs).

Usage:
  python3 assemble.py [--root DIR] [--title "Deck Name"]            # build deck.html
  python3 assemble.py [--root DIR] --shots                          # build + render every slide to shots/sNN.png
  python3 assemble.py [--root DIR] --preview sNN.html               # wrap ONE fragment, screenshot to shots/sNN.png
"""
import sys as _s
if "-h" in _s.argv or "--help" in _s.argv:
    print(__doc__); _s.exit(0)
import re, sys, os, shutil, subprocess, pathlib

def _arg(flag, default=None):
    if flag in sys.argv:
        i = sys.argv.index(flag); v = sys.argv[i + 1]; del sys.argv[i:i + 2]; return v
    return default

ROOT = pathlib.Path(_arg("--root", os.environ.get("DECK_ROOT", "."))).resolve()
TITLE = _arg("--title", "Deck")
SLIDES = ROOT / "slides"
(ROOT / "build").mkdir(exist_ok=True); (ROOT / "shots").mkdir(exist_ok=True)
CSS = (ROOT / "assets" / "deck.css").read_text()
CHROME = next((c for c in [os.environ.get("CHROME"),
                           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                           shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser")] if c and os.path.exists(c)), None)
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600'
         '&family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap">')

TIP_JS = """
<div id="tip" hidden></div>
<script>
window.DeckTip = (function(){
  const tip = document.getElementById('tip');
  function move(e){ const x=Math.min(e.clientX+14, window.innerWidth-310); tip.style.left=x+'px'; tip.style.top=(e.clientY+14)+'px'; }
  return {
    attach(el, html){ el.addEventListener('mouseenter', e=>{tip.innerHTML=html; tip.hidden=false; move(e);});
                      el.addEventListener('mousemove', move); el.addEventListener('mouseleave', ()=>{tip.hidden=true;}); }
  };
})();
</script>
"""

NAV_JS = """
<script>
(function(){
  const slides=[...document.querySelectorAll('.slide')];
  const deck=document.querySelector('.deck');
  const pos=document.getElementById('pos');
  let i=0;
  function fit(){
    if(!document.body.classList.contains('present')){ deck.style.transform=''; deck.style.height=''; return; }
    const bar=document.querySelector('.deck-bar'); const bh=bar?bar.getBoundingClientRect().height:0;
    const s=Math.min(window.innerWidth/1282, (window.innerHeight-bh)/722);
    deck.style.transform='scale('+s+')'; deck.style.transformOrigin='top center';
  }
  function show(k){
    i=Math.max(0,Math.min(slides.length-1,k));
    slides.forEach((s,j)=>s.classList.toggle('active', j===i));
    pos.textContent=(i+1)+' / '+slides.length+' · '+(slides[i].dataset.title||'');
    try{ history.replaceState(null,'','#'+slides[i].id); }catch(e){}
    if(!document.body.classList.contains('present')) slides[i].scrollIntoView({block:'start'});
  }
  function toggle(){ document.body.classList.toggle('present'); slides.forEach(sl=>{ sl.style.zoom=''; }); fitScroll(); fit(); show(i); }
  document.getElementById('mode').addEventListener('click', toggle);
  document.getElementById('prev').addEventListener('click', ()=>show(i-1));
  document.getElementById('next').addEventListener('click', ()=>show(i+1));
  document.addEventListener('keydown', e=>{
    const t=e.target; if(t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(t.tagName))) return;
    const pres=document.body.classList.contains('present');
    if(e.key==='ArrowRight'||e.key==='PageDown'||(e.key===' '&&pres)){ e.preventDefault(); show(i+1); }
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){ e.preventDefault(); show(i-1); }
    else if(e.key==='Home'){ e.preventDefault(); show(0); }
    else if(e.key==='End'){ e.preventDefault(); show(slides.length-1); }
    else if(e.key==='p'||e.key==='P'){ toggle(); }
    else if(e.key==='Escape'&&pres){ toggle(); }
  });
  let tx=null;
  document.addEventListener('touchstart', e=>{ if(document.body.classList.contains('present')) tx=e.touches[0].clientX; }, {passive:true});
  document.addEventListener('touchend', e=>{ if(tx===null) return; const dx=e.changedTouches[0].clientX-tx; tx=null; if(Math.abs(dx)>40) show(i+(dx<0?1:-1)); }, {passive:true});
  window.addEventListener('resize', fit);
  const h=(location.hash||'').slice(1); const k=slides.findIndex(s=>s.id===h);
  // scale slides down to fit narrow screens in scroll mode
  function fitScroll(){
    if(document.body.classList.contains('present')) return;
    const s=Math.min(1,(window.innerWidth-24)/1282);
    slides.forEach(sl=>{ sl.style.zoom = s<1 ? s : ''; });
  }
  window.addEventListener('resize', fitScroll); fitScroll();
  show(k>=0?k:0);
})();
</script>
"""

def page(body, title=None, chrome=True):
    title = title or TITLE
    bar = ('<div class="deck-bar"><span id="pos"></span><span>'
           '<button id="prev" aria-label="Previous slide">←</button> '
           '<button id="next" aria-label="Next slide">→</button> '
           '<button id="mode">Present (P)</button></span></div>') if chrome else ''
    return (f"<title>{title}</title>\n{FONTS}\n<style>\n{CSS}\n</style>\n{bar}\n{TIP_JS}\n"
            f'<div class="deck">\n{body}\n</div>\n' + (NAV_JS if chrome else ''))

def fragments():
    return sorted(SLIDES.glob("s[0-9][0-9].html"))

def shot(html_path, png_path, h=760):
    if not CHROME:
        print("no Chrome/Chromium found; set CHROME=/path/to/chrome"); return
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size=1340,{h}", "--virtual-time-budget=5000",
                    f"--screenshot={png_path}", f"file://{html_path}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def build(with_shots=False):
    frags = fragments()
    body = "\n".join(f.read_text() for f in frags)
    out = ROOT / "deck.html"
    out.write_text(page(body))
    print(f"wrote {out} with {len(frags)} slides")
    if with_shots:
        for f in frags:
            p = ROOT / "build" / f"preview_{f.stem}.html"
            p.write_text(page(f.read_text(), chrome=False))
            shot(p, ROOT / "shots" / f"{f.stem}.png")
        print("shots in", ROOT / "shots")

def preview(name):
    f = SLIDES / name
    p = ROOT / "build" / f"preview_{f.stem}.html"
    p.write_text(page(f.read_text(), chrome=False))
    png = ROOT / "shots" / f"{f.stem}.png"
    shot(p, png)
    print("preview:", p, "\nscreenshot:", png)

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        preview(sys.argv[2])
    else:
        build("--shots" in sys.argv)
