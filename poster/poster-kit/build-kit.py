#!/usr/bin/env python3
"""Generate a self-contained, modular SVG poster kit for Claude Design.
Units: millimetres. A0 portrait = 841 x 1189 mm. Origin top-left, y down.

Body copy is auto-wrapped to fill the available width (measured against the
real STIX Two Text metrics) so there are no hand-forced line breaks."""
import base64, json, os, re, html
from PIL import Image, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(KIT, "figures")
MOD = os.path.join(KIT, "modules")
os.makedirs(MOD, exist_ok=True)

# ---------- palette ----------
DARK="#1B4F72"; AMBER="#D68910"; RED="#C0392B"; GREEN="#1E8449"
BLUE2="#2E86C1"; GRAY="#7F8C8D"; LIGHT="#F4F6F7"; INK="#1A1A1A"
L_BLUE="#D6EAF8"; L_BLUE2="#AED6F1"
FONT="'STIX Two Text','Times New Roman',Georgia,serif"
PT=0.3528  # pt -> mm
# force lining (not old-style) figures so numerals sit on the caps baseline
LNUM='font-variant-numeric:lining-nums;font-feature-settings:&#39;lnum&#39; 1;'

# real-font metrics for accurate word-wrap (STIX Two Text = the poster face)
_METRIC=ImageFont.truetype("/System/Library/Fonts/Supplemental/STIXTwoText.ttf",1000)
def strw(s,size):            # rendered width in mm at font-size `size` mm
    return _METRIC.getlength(s)/1000.0*size
def wrap(text,avail,size):   # greedy word-wrap to fill `avail` mm
    out=[]; cur=""
    for word in text.split():
        cand=(cur+" "+word).strip()
        if not cur or strw(cand,size)<=avail:
            cur=cand
        else:
            out.append(cur); cur=word
    if cur: out.append(cur)
    return out

def esc(s): return html.escape(s, quote=True)

# Auto-subscript: turn `X_sub` (single base letter + 1-3 letter subscript, e.g.
# R_eff, V_d, C_v) into a real typographic subscript. Applied to every string that
# flows through T() (and therefore lines()/para()), so no call site needs markup.
SUBRE=re.compile(r'([A-Za-z])_([A-Za-z]{1,3})\b')
def subify(s,sz):
    out=[]; i=0
    for m in SUBRE.finditer(s):
        out.append(esc(s[i:m.start()])+esc(m.group(1)))
        out.append(f'<tspan font-size="{sz*0.62:.2f}" baseline-shift="-18%">'
                   f'{esc(m.group(2))}</tspan>')
        i=m.end()
    out.append(esc(s[i:]))
    return "".join(out)

_ANCHORS=("start","middle","end")
def T(x,y,s,sz,fill=INK,w="normal",it=False,anc="start",style=""):
    # Harden: `it` sits before `anc` in the signature, so an anchor passed
    # positionally (T(...,"bold","middle")) silently lands in `it` — left-anchoring
    # the text and italicising it. Detect and reroute rather than fail silently.
    if isinstance(it,str) and it in _ANCHORS:
        anc=it; it=False
    assert anc in _ANCHORS, f"T(): bad text-anchor {anc!r}"
    st="italic" if it else "normal"
    stattr=f' style="{style}"' if style else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" '
            f'font-size="{sz:.2f}" fill="{fill}" font-weight="{w}" '
            f'font-style="{st}" text-anchor="{anc}"{stattr}>{subify(s,sz)}</text>')

def lines(x,y,arr,sz,fill=INK,w="normal",it=False,lh=1.32,anc="start"):
    out=[]
    for i,s in enumerate(arr):
        out.append(T(x, y+i*sz*lh, s, sz, fill, w, it, anc))
    return "\n".join(out)

def para(x,y,text,sz,avail,fill=INK,w="normal",it=False,lh=1.32,anc="start"):
    """Auto-wrapped paragraph. Returns (svg, n_lines, baseline_of_last_line)."""
    arr=wrap(text,avail,sz)
    return lines(x,y,arr,sz,fill,w,it,lh,anc), len(arr), y+(len(arr)-1)*sz*lh

def R(x,y,w,h,fill,stroke="none",sw=0,rx=0,op=1):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'opacity="{op}"/>')

def img(path,x,y,w):
    im=Image.open(path); iw,ih=im.size; h=w*ih/iw
    with open(path,"rb") as f: b=base64.b64encode(f.read()).decode()
    return (f'<image x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'preserveAspectRatio="xMidYMid meet" '
            f'xlink:href="data:image/png;base64,{b}"/>'), h

def vsvg(path,x,y,w):
    """Inline a true-vector figure composite (its IDs are pre-namespaced per figure,
    so multiple vsvg() calls never collide) as a nested <svg> scaled to width `w` mm."""
    s=open(path).read()
    vbx,vby,vbw,vbh=map(float,re.search(r'viewBox="([0-9.\s-]+)"',s).group(1).split())
    h=w*vbh/vbw
    body=re.sub(r'</svg>\s*$','',re.sub(r'^.*?<svg[^>]*>','',s,count=1,flags=re.DOTALL),
                flags=re.DOTALL)
    return (f'<svg x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'viewBox="0 0 {vbw:.2f} {vbh:.2f}" preserveAspectRatio="xMidYMid meet" '
            f'overflow="visible">{body}</svg>'), h

def rsub(x,y,base,sub,sz,fill=INK,w="normal",anc="start"):
    """R with subscript, e.g. R_eff."""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{sz:.2f}" '
            f'fill="{fill}" font-weight="{w}" text-anchor="{anc}">{esc(base)}'
            f'<tspan font-size="{sz*0.62:.2f}" baseline-shift="-18%">{esc(sub)}</tspan></text>')

# QR vector path
qr_raw=open(os.path.join(FIG,"qr.svg")).read()
qr_path=re.search(r'<path d="([^"]+)"', qr_raw).group(1)
def qr_group(x,y,size):
    s=size/31.0
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.4f})">'
            f'<rect x="0" y="0" width="31" height="31" fill="#FFFFFF"/>'
            f'<path d="{qr_path}" fill="{DARK}"/></g>')

def svg_wrap(W,H,inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n{inner}\n</svg>\n')

# ===================== MODULES =====================
modules={}   # name -> (W,H,inner)

# ---- 00 header (841 x 120) ----
W,H=841,120; p=[]
p.append(R(0,0,W,H,DARK))
p.append(T(30,56,"Civilizational Metamaterials",35,"#FFFFFF","bold"))
p.append(T(30,80,"Engineering Coordination Under Capability Gradients and Structural Turbulence",11.6,L_BLUE,it=True))
p.append(T(30,99,"David Orban   ·   Independent Researcher   ·   ORCID 0009-0004-4954-1147",9.2,L_BLUE2))
p.append(T(811,54,"AGI-26",15,AMBER,"bold",anc="end",style=LNUM))
# the two conference lines tightened together (were too far apart)
p.append(T(811,76,"19th Conference on Artificial General Intelligence",7.4,L_BLUE,anc="end",style=LNUM))
p.append(T(811,86,"San Francisco State University · July 27–30, 2026",7.4,L_BLUE,anc="end",style=LNUM))
modules["00-header"]=(W,H,"\n".join(p))

# ---- 01 central claim (791 x 128) ----
W,H=791,128; p=[]
p.append(R(0,0,W,H,LIGHT,DARK,2,6))
p.append(T(20,20,"THE CENTRAL CLAIM",8.5,AMBER,"bold"))
svg,_,_=para(20,38,
 "AGI raises decision velocity exponentially while human verification stays bounded. "
 "The fix is not more intelligence: it is structure. Governance must become an engineering "
 "discipline that designs coordination microstructures to keep error propagation sub-critical:",
 9.5,751,INK,lh=1.34)
p.append(svg)
eq=(f'<text x="{W/2:.2f}" y="86" font-family="{FONT}" font-size="20.5" fill="{DARK}" '
    f'font-weight="bold" text-anchor="middle">R'
    f'<tspan font-size="12.7" baseline-shift="-18%">eff</tspan>'
    f' = β (1−ρ)(1−τ)(1−γρτ)</text>')
p.append(eq)
p.append(T(W/2,112,"β branching factor   ·   ρ provenance fidelity   ·   τ verification rate   ·   γ correlated-detection synergy",7.6,GRAY,anc="middle"))
modules["01-central-claim"]=(W,H,"\n".join(p))

# ---- column helper header bar (text vertically centred on the coloured bar) ----
def col_head(n,title,color,W=247,barh=16):
    ty=barh/2+2.98    # centre caps on the bar
    return (R(0,0,W,barh,color,rx=3)+"\n"+
            T(6,ty,f"{n}  {title}",8.5,"#FFFFFF","bold",style=LNUM))

# common top edge for the three lower "summary" cards, so they align across columns
CARD_TOP=258
def card_h(nlines):           # height for a titled card holding `nlines` body lines
    return round(28+(nlines-1)*9.1+8)

# ---- 02 column problem ----
p=[]
p.append(col_head("1","THE PROBLEM",RED))
p.append(T(0,31,"Decision–Verification Decoupling",8.8,DARK,"bold"))
svg,_,_=para(0,44,
 "Decisions branch downstream at machine speed. Verification is capped by human cognition. "
 "The gap does not close; it widens after the AGI transition, and error can cascade faster "
 "than any institution can audit it.",7.1,245,INK,lh=1.32)
p.append(svg)
im,fh=img(os.path.join(FIG,"fig1.png"),0,90,247)
p.append(im)
p.append(T(0,90+fh+6,"Fig 1 · Decision velocity (V_d) vs. verification velocity (C_v).",5.6,GRAY,it=True))
by=CARD_TOP
fz,nfz,_=para(7,by+26,
 "When the cost of validating an AI output exceeds the expected utility of acting on it, "
 "rational agents default to inaction: a stable but catastrophic Nash equilibrium. "
 "Paralysis, not error, becomes the dominant failure mode.",7.0,233,INK,lh=1.30)
hfz=card_h(nfz)
p.append(R(0,by,247,hfz,"#FDEDEC",RED,1.5,4))
p.append(T(7,by+14,"The Freezing Equilibrium",8.1,RED,"bold"))
p.append(fz)
modules["02-column-problem"]=(247,by+hfz+6,"\n".join(p))

# ---- 03 column phase ----
p=[]
p.append(col_head("2","THE PHASE TRANSITION",DARK))
svg,_,yend=para(0,31,
 "The constitutive law predicts a sharp transition at R_eff = 1, the institutional analog "
 "of a metamaterial bandgap.",7.1,245,INK,lh=1.32)
p.append(svg)
im,fh=vsvg(os.path.join(FIG,"fig2.svg"),18,52,210)
p.append(im); ycap=52+fh+6
# Fig 2 caption on a single line — fit the type size to the column width
cap2="Fig 2 · R_eff across the (ρ, τ) plane. Blue = damped (self-healing); red = turbulent (self-destabilizing)."
csz=5.6
while strw(cap2,csz)>247 and csz>4.6: csz-=0.1
p.append(T(0,ycap,cap2,csz,GRAY,it=True))
by=CARD_TOP
p.append(R(0,by,247,96,LIGHT,DARK,1.5,4))
p.append(T(7,by+14,"Two regimes",8.1,DARK,"bold"))
p.append(rsub(7,by+27,"R","eff",7.1,INK)+T(20,by+27,"< 1:  errors decay, institutions self-heal.",7.1,INK))
p.append(rsub(7,by+37,"R","eff",7.1,INK)+T(20,by+37,"> 1:  errors amplify, coordination collapses.",7.1,INK))
syn,_,_=para(7,by+50,
 "Correlated detection (1−γρτ): because γρτ grows with both controls at once, high ρ and high τ "
 "together cross into the damped regime where either alone stays turbulent.",6.8,233,INK,lh=1.30)
p.append(syn)
p.append(T(7,by+88,"Worked example (β=10, ρ=0.5, γ=1):  τ* ≈ 0.69.",6.9,DARK,"bold"))
modules["03-column-phase"]=(247,by+96+6,"\n".join(p))

# ---- 04 column framework ----
p=[]
p.append(col_head("3","THE FRAMEWORK",GREEN))
p.append(T(0,31,"A three-class provenance taxonomy",8.4,DARK,"bold"))
# three provenance-class cards, spaced like the H1–H4 stack (gap ≈ 11mm, was 4)
cgap=11
ayA=38                       # Class A top
ayB=ayA+26+cgap              # Class B top = 75
ayC=ayB+26+cgap              # Class C top = 112
# Class A
p.append(R(0,ayA,247,26,"#EAF2F8",BLUE2,1.2,3))
p.append(T(6,ayA+12,"Class A · Cryptographic",7.4,BLUE2,"bold"))
p.append(T(6,ayA+22,"C2PA manifests · signatures · hash assertions",6.4,INK))
# Class B
p.append(R(0,ayB,247,26,"#FEF5E7",AMBER,1.2,3))
p.append(T(6,ayB+12,"Class B · Institutional",7.4,AMBER,"bold"))
p.append(T(6,ayB+22,"SCITT receipts · Merkle trees · reputation",6.4,INK))
# Class C novel — NOVEL pill centred (horizontally + vertically) in its green rect
p.append(R(0,ayC,247,28,"#E9F7EF",GREEN,2.5,3))
pill_w=40; pill_h=9; pill_x=247-4-pill_w; pill_y=ayC+(28-pill_h)/2
p.append(R(pill_x,pill_y,pill_w,pill_h,GREEN,rx=4))
p.append(T(pill_x+pill_w/2,pill_y+pill_h/2+2.0,"NOVEL",5.6,"#FFFFFF","bold",anc="middle"))
p.append(T(6,ayC+13,"Class C · Context Binding",7.4,GREEN,"bold"))
p.append(T(6,ayC+23,"SRC anchors · temporal scope · jurisdiction",6.4,INK))
# synthetic principals (shifted down: Class C card now ends at y=140, was 126)
p.append(T(0,157,"Synthetic principals",7.8,DARK,"bold"))
svg,_,_=para(0,168,
 "AI agents act as principals, not mere tools, inside decision networks, each requiring its "
 "own provenance, delegation limits and audit trail.",7.0,245,INK,lh=1.30)
p.append(svg)
# trust anchors
p.append(T(0,200,"Layered trust anchors",7.8,DARK,"bold"))
svg,_,_=para(0,211,
 "Constitutional commitments → distributed consensus → treaty bodies → verification markets: "
 "a defense-in-depth answer to “who guards the guardians?”",7.0,232,INK,lh=1.30)
p.append(svg)
# design levers card — aligned top with the other two summary cards
by=CARD_TOP
dl,ndl,_=para(7,by+26,
 "Lower β · raise ρ · raise τ: together, not alone. Correlated detection (1−γρτ) rewards moving "
 "ρ and τ jointly, so the pair crosses into the damped regime where neither alone would.",7.0,233,INK,lh=1.30)
hdl=card_h(ndl)
p.append(R(0,by,247,hdl,"#EBF5FB",DARK,1.5,4))
p.append(T(7,by+14,"Design levers",8.1,DARK,"bold"))
p.append(dl)
modules["04-column-framework"]=(247,by+hdl+6,"\n".join(p))

# ---- 05 testing band (791 x 304) — bigger Fig 7, taller & narrower H cards ----
W,H=791,304; p=[]
p.append(R(0,0,W,H,"#FBFCFC",GRAY,1.2,5))
p.append(T(18,30,"TESTING THE FRAMEWORK",9.2,DARK,"bold"))
p.append(T(18,45,"Four falsifiable hypotheses · a 12-week stepped-wedge cluster-RCT across government R&D grant-review panels.",7.4,GRAY,it=True))
FIG7_W=340; FIG7_Y=56
im,fh=vsvg(os.path.join(FIG,"fig7.svg"),18,FIG7_Y,FIG7_W)
p.append(im)
p.append(T(18,FIG7_Y+fh+7,"Fig 7 · Stepped-wedge crossover schedule.",5.6,GRAY,it=True))
hyps=[("H1","Bandgap Effect",RED,
   "Scaffolded pipelines show exponential (not power-law) error-propagation depth; failure modes forbidden by structure."),
  ("H2","Coordination Anisotropy",AMBER,
   "A system can be locally stable yet unstable across boundaries (R_eff intra < 1, R_eff cross > 1) at the same time."),
  ("H3","Superadditivity",GREEN,
   "In a 2×2 ρ×τ factorial, only the high–high condition reaches self-healing (exponential cascade decay); single interventions stay turbulent (γ > 0)."),
  ("H4","Structural Hysteresis",BLUE2,
   "Recovery time after withdrawing scaffolding exceeds original adoption time by a factor > 3.")]
hx=376; hw=W-hx-18; ch=40; gap=12           # narrower cards → more room for Fig 7; taller so text clears the base
dlh=6.2*1.24
stack=len(hyps)*ch+(len(hyps)-1)*gap
cy=FIG7_Y+(fh-stack)/2                       # centre the card stack on the figure
for tag,name,col,desc in hyps:
    dlines=wrap(desc,hw-44,6.2)
    block=7.8+3+ (len(dlines)-1)*dlh + 2     # name + gap + desc lines
    top=cy+(ch-block)/2                       # vertically centre the text block
    p.append(R(hx,cy,hw,ch,"#FFFFFF",col,1.5,3))
    p.append(R(hx,cy,30,ch,col,rx=3))
    p.append(T(hx+15,cy+ch/2+3.2,tag,9.2,"#FFFFFF","bold",anc="middle",style=LNUM))
    p.append(T(hx+38,top+6.2,name,7.8,col,"bold"))
    p.append(lines(hx+38,top+6.2+9,dlines,6.2,INK,lh=1.24))
    cy+=ch+gap
modules["05-testing-band"]=(W,H,"\n".join(p))

# ---- 06 footer (841 x 237) ----
W,H=841,237; p=[]
p.append(R(0,0,W,H,DARK))
p.append(T(30,38,"THE TAKEAWAY",8.5,AMBER,"bold"))
svg,_,_=para(30,56,
 "Treat coordination as a material to be engineered. Specify the microstructure: provenance, "
 "verification, delegation limits; so the macroscopic property you need (R_eff < 1) emerges "
 "by design rather than by hope. Governance becomes falsifiable, measurable, and buildable.",
 9.5,660,"#FFFFFF",lh=1.32)
p.append(svg)
p.append(T(30,116,"Paper, code, reference implementation and an interactive R_eff explorer:",7.8,L_BLUE2))
p.append(T(30,134,"metamaterials.davidorban.com",9.2,"#FFFFFF","bold"))
p.append(T(30,152,"DOI 10.5281/zenodo.19710482   ·   github.com/davidorban/civilizationalmetamaterials",7.4,L_BLUE,style=LNUM))
p.append(T(30,176,"Bridging AI alignment theory and institutional design.",7.4,L_BLUE2,it=True))
p.append(qr_group(715,28,96))
p.append(T(763,138,"Scan for paper + tools",6.0,L_BLUE2,anc="middle"))
modules["06-footer"]=(W,H,"\n".join(p))

# ===================== WRITE MODULES =====================
order=["00-header","01-central-claim","02-column-problem","03-column-phase",
       "04-column-framework","05-testing-band","06-footer"]
for name in order:
    W,Hh,inner=modules[name]
    open(os.path.join(MOD,name+".svg"),"w").write(svg_wrap(W,Hh,inner))

# ===================== MASTER (A0) =====================
PW,PH=841,1189
place={  # name: (x,y)
 "00-header":(0,0),
 "01-central-claim":(25,132),
 "02-column-problem":(25,270),
 "03-column-phase":(297,270),
 "04-column-framework":(569,270),
 "05-testing-band":(25,640),
 "06-footer":(0,952),
}
parts=[f'<rect x="0" y="0" width="{PW}" height="{PH}" fill="#FFFFFF"/>']
for name in order:
    W,Hh,inner=modules[name]; x,y=place[name]
    parts.append(f'<svg x="{x}" y="{y}" width="{W}" height="{Hh}" '
                 f'viewBox="0 0 {W} {Hh}" overflow="visible">\n{inner}\n</svg>')
master=svg_wrap(PW,PH,"\n".join(parts))
open(os.path.join(KIT,"poster-master.svg"),"w").write(master)

# ===================== MANIFEST =====================
def mh(name): return modules[name][1]
manifest={
 "canvas":{"format":"A0 portrait","width_mm":PW,"height_mm":PH,
   "units":"mm","origin":"top-left","bleed_mm":3,"safe_margin_mm":20,
   "color_space":"sRGB authoring; convert to CMYK at print (FOGRA39/GRACoL)"},
 "fonts":{"family":"STIX Two Text (serif); fallback Times/Georgia",
   "note":"All text is live <text>; body copy auto-wrapped to width; numerals forced to lining figures; embed/outline fonts before final print."},
 "palette":{"dark_blue":DARK,"amber":AMBER,"red":RED,"green":GREEN,
   "blue2":BLUE2,"gray":GRAY,"light":LIGHT,"ink":INK},
 "type_scale_pt":{"title":99,"subtitle":33,"agi_lockup":42,"central_body":27,
   "equation":58,"column_header":24,"subhead":23,"body":20,"hyp_tag":26,
   "hyp_name":22,"caption":16,"footer_body":27,"url":26},
 "grid":{"body_margin_mm":25,"columns":3,"column_width_mm":247,"gutter_mm":25},
 "modules":[
  {"file":"modules/00-header.svg","w_mm":841,"h_mm":mh("00-header"),"x_mm":0,"y_mm":0,
   "bleeds":True,"role":"Title, author, conference lockup"},
  {"file":"modules/01-central-claim.svg","w_mm":791,"h_mm":mh("01-central-claim"),"x_mm":25,"y_mm":132,
   "role":"Thesis + dominant equation + parameter legend"},
  {"file":"modules/02-column-problem.svg","w_mm":247,"h_mm":mh("02-column-problem"),"x_mm":25,"y_mm":270,
   "figure":"fig1.png","role":"Problem: decoupling, Fig 1, Freezing Equilibrium"},
  {"file":"modules/03-column-phase.svg","w_mm":247,"h_mm":mh("03-column-phase"),"x_mm":297,"y_mm":270,
   "figure":"fig2.png","role":"Phase transition: Fig 2 (dominant graphic), two regimes"},
  {"file":"modules/04-column-framework.svg","w_mm":247,"h_mm":mh("04-column-framework"),"x_mm":569,"y_mm":270,
   "role":"Framework: provenance taxonomy, synthetic principals, trust anchors"},
  {"file":"modules/05-testing-band.svg","w_mm":791,"h_mm":mh("05-testing-band"),"x_mm":25,"y_mm":640,
   "figure":"fig7.png","role":"Fig 7 (enlarged) + four hypothesis cards H1–H4"},
  {"file":"modules/06-footer.svg","w_mm":841,"h_mm":mh("06-footer"),"x_mm":0,"y_mm":952,
   "bleeds":True,"figure":"qr.svg (vector)","role":"Takeaway, links, QR"},
 ],
 "figures":{
   "fig1.png":"raster 1950×1200 (V_d-fix composite) — swap for vector if regenerated",
   "fig2.svg":"HYBRID VECTOR: vector axes/labels/boundary/markers/colorbar/inset over a high-DPI rasterized heatmap gradient (viewBox 468×396 pt)",
   "fig7.svg":"TRUE VECTOR: stepped-wedge trial design, fully vector (viewBox 576×396 pt)",
   "qr.svg":"TRUE VECTOR path → https://metamaterials.davidorban.com"},
 "reading_path":"title → central claim → col1 → col2 → col3 → testing band → footer",
}
open(os.path.join(KIT,"manifest.json"),"w").write(json.dumps(manifest,indent=2,ensure_ascii=False))
print("KIT WRITTEN")
for name in order:
    f=os.path.join(MOD,name+".svg"); print(name, mh(name),"mm", os.path.getsize(f),"bytes")
print("master", os.path.getsize(os.path.join(KIT,"poster-master.svg")),"bytes")
