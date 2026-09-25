"""Erzeugt die gerechneten Bausteine: Quotient D4 -> V4 mit Sphären; Phasenkreis Z8."""
import os, json, math, itertools
out=os.path.join(os.path.dirname(__file__),'..','tex','bausteine'); os.makedirs(out,exist_ok=True)
erg=json.load(open(os.path.join(os.path.dirname(__file__),'ergebnis_vorzeichen.json')))

# ---- Baustein 1: D4 (Cl(2,0)) und Quotient V4 = Sphären ----
def mul(a,b):
    sa,Sa=a; sb,Sb=b; s=sa*sb
    if (Sa&2) and (Sb&1): s=-s
    return (s,Sa^Sb)
G=[(s,S) for s in (1,-1) for S in range(4)]; E=(1,0)
def order(g):
    x=g;n=1
    while x!=E: x=mul(x,g); n+=1
    return n
name={(1,0):'1',(-1,0):'-1',(1,1):'e_1',(-1,1):'-e_1',(1,2):'e_2',(-1,2):'-e_2',(1,3):'\\omega',(-1,3):'-\\omega'}
sph={0:'S_1',1:'S_2',2:'S_3',3:'S_4'}
L=["% GERECHNET von erzeuge_bausteine.py — Gruppe, Ordnungen, Quotient aus der Erzeugerrelation, nicht von Hand",
   "\\begin{tikzpicture}[>=Stealth,el/.style={circle,draw,fill=white,inner sep=1pt,font=\\small,minimum size=7.5mm},q/.style={rectangle,draw,rounded corners=2pt,fill=grau!8,inner sep=3pt,font=\\small,minimum width=1.5cm,minimum height=7mm}]"]
# obere Reihe: die acht, nach Klassen gruppiert (Spalten S=0..3), Vorzeichen oben/unten
for S in range(4):
    x=2.2*S
    for s,y in ((1,1.0),(-1,-1.0)):
        g=(s,S); L.append(f"\\node[el] (g{S}{'p' if s>0 else 'm'}) at ({x},{y}) {{${name[g]}$}};")
    L.append(f"\\draw[grau,dashed] (g{S}p)--(g{S}m);")
    L.append(f"\\node[q] (q{S}) at ({x},-3.2) {{${sph[S]}$}};")
    L.append(f"\\draw[->,thick,grau] ({x},-1.5)--({x},-2.75);")
# Takte beschriften
for S in range(4):
    o=order((1,S)); L.append(f"\\node[font=\\scriptsize,grau,anchor=south] at ({2.2*S},1.5) {{Takt {o}}};")
L.append("\\node[font=\\scriptsize,anchor=east] at (-0.9,0) {Geacht der Form};")
L.append("\\node[font=\\scriptsize,anchor=east] at (-0.9,-3.2) {Sphären};")
L.append("\\node[font=\\scriptsize,grau,anchor=east] at (-0.9,-2.1) {$\\pm1$ vergessen};")
L.append("\\node[font=\\scriptsize,align=center,anchor=north] at (3.3,-3.8) {$e_1e_2=-e_2e_1$, $\\omega^2=-1$ \\quad$\\longmapsto$\\quad $S_2S_3=S_3S_2=S_4$, $S_4^2=S_1$};")
L.append("\\end{tikzpicture}")
open(os.path.join(out,'baustein_quotient.tex'),'w').write("\n".join(L)+"\n")

# ---- Baustein 2: Phasenkreis Z8 ----
sech={'\\hbar':(0,0),'c^{-1}':(1,-1),'c':(-1,1),'c^2':(-2,2),'F':(-1,-1),'L^{-2}':(0,-2),'P':(-2,0),'p':(-1,-3),
      'm':(1,-2),'T':(1,0),'L':(0,1),'k':(0,-1),'\\nu':(-1,0),'\\hbar/m':(-1,2),'a':(-2,1),'V':(0,3)}
leit={'q':(-0.5,0.5),'\\psi':(0,-1.5),'q\\psi':(-0.5,-1.0)}
ph=lambda b:(int(round(2*b)))%8
R=2.4
L=["% GERECHNET von erzeuge_bausteine.py — Phasen i^b aus den Exponenten, nicht von Hand",
   "\\begin{tikzpicture}[>=Stealth]",f"\\draw[thick,grau] (0,0) circle ({R});"]
for k in range(8):
    ang=45*k; x=R*math.cos(math.radians(ang)); y=R*math.sin(math.radians(ang))
    col="zeit" if k%2==0 else "raum"
    L.append(f"\\fill[{col}] ({x:.3f},{y:.3f}) circle (2pt);")
lab={0:'1',2:'i',4:'-1',6:'-i'}
for k,t in lab.items():
    ang=45*k; x=(R+0.35)*math.cos(math.radians(ang)); y=(R+0.35)*math.sin(math.radians(ang))
    L.append(f"\\node[font=\\small,zeit!80!black] at ({x:.3f},{y:.3f}) {{${t}$}};")
kl={}
for n,(a,b) in sech.items(): kl.setdefault(ph(b),[]).append(n)
for k,names in kl.items():
    ang=45*k; x=(R+1.25)*math.cos(math.radians(ang)); y=(R+1.25)*math.sin(math.radians(ang))
    L.append(f"\\node[font=\\scriptsize,align=center] at ({x:.3f},{y:.3f}) {{${'$, $'.join(names)}$}};")
for n,(a,b) in leit.items():
    k=ph(b); ang=45*k; x=(R-0.6)*math.cos(math.radians(ang)); y=(R-0.6)*math.sin(math.radians(ang))
    L.append(f"\\node[font=\\small,raum!80!black,fill=white,inner sep=1pt] at ({x:.3f},{y:.3f}) {{${n}$}};")
L.append("\\node[font=\\scriptsize,align=center] at (0,0) {Phase $i^{\\,b}$\\\\unter $L=iT$};")
L.append("\\end{tikzpicture}")
open(os.path.join(out,'baustein_phasen.tex'),'w').write("\n".join(L)+"\n")
print("ok", os.listdir(out))
