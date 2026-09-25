"""Erzeugt die gerechneten TikZ-Bausteine: Geacht der Form, Fano beidseitig."""
import itertools, numpy as np, os
out=os.path.join(os.path.dirname(__file__),'..','tex','bausteine')
os.makedirs(out,exist_ok=True)

# ---- Geacht der Form: Gruppe aus e1,e2 mit e_i^2=+1, e1e2=-e2e1, als Paare (Vorzeichen, Blade) ----
def mul(a,b):
    sa,Sa=a; sb,Sb=b
    sign=sa*sb
    # Antivertauschung: e2*e1 = -e1*e2
    if Sa==2 and (Sb&1): sign=-sign
    if Sa==3 and (Sb&1): sign=-sign  # (e1e2)e1 = -e1(e1e2)... allgemein per Bitregel:
    # exakte Bitregel
    sign=sa*sb
    for i in range(2):
        if Sa>>i&1:
            for j in range(i):
                if Sb>>j&1: sign=-sign
    # Erzeuger mit Quadrat +1 (Wechsel), wie in der Lehre von den Zeilen: Cl(2,0); dann omega^2=-1
    return (sign,Sa^Sb)
G=[(s,S) for s in (1,-1) for S in range(4)]
assert len({mul(a,b) for a in G for b in G})==8
def order(g):
    x=g;n=1
    while x!=(1,0): x=mul(x,g); n+=1
    return n
orders={g:order(g) for g in G}
assert sorted(orders.values())==[1,2,2,2,2,2,4,4]
subgroups=[]
for combo in itertools.combinations(G,4):
    S=set(combo)
    if (1,0) in S and all(mul(a,b) in S for a in S for b in S): subgroups.append(frozenset(S))
assert len(subgroups)==3
name={ (1,0):'1',(-1,0):'-1',(1,1):'e_1',(-1,1):'-e_1',(1,2):'e_2',(-1,2):'-e_2',(1,3):'\\omega',(-1,3):'-\\omega'}
cyc=[S for S in subgroups if any(orders[g]==4 for g in S)][0]
kl=[S for S in subgroups if S!=cyc]
lines=[]
lines.append("% GERECHNET von erzeuge_bausteine.py — Gruppe, Ordnungen und Untergruppen aus der Erzeugerrelation, nicht von Hand")
lines.append("\\begin{tikzpicture}[>=Stealth,el/.style={circle,draw,fill=white,inner sep=1.5pt,font=\\small,minimum size=8mm}]")
# Umlauf-Geviert als Kreis in der Mitte, Kleinsche als Ellipsen links/rechts
pos={(1,0):(0,1.1),(-1,0):(0,-1.1),(1,3):(1.1,0),(-1,3):(-1.1,0),(1,1):(-3.2,1.1),(-1,1):(-3.2,-1.1),(1,2):(3.2,1.1),(-1,2):(3.2,-1.1)}
lines.append("\\draw[thick,zeit] (0,0) circle (1.1);")
lines.append("\\draw[thick,raum,rounded corners=8pt] (-3.9,1.7) rectangle (0.6,-1.7);")
lines.append("\\draw[thick,ferm,rounded corners=8pt] (-0.6,1.7) rectangle (3.9,-1.7);")
for g,(x,y) in pos.items():
    lines.append(f"\\node[el] at ({x},{y}) {{${name[g]}$}};")
cyc_names=" \\to ".join(name[g] for g in [(1,0),(1,3),(-1,0),(-1,3)])
lines.append(f"\\node[font=\\scriptsize,zeit,anchor=north] at (0,-1.85) {{Umlauf: ${cyc_names}\\to 1$ (Takt {orders[(1,3)]})}};")
lines.append("\\node[font=\\scriptsize,raum,anchor=south] at (-2.2,1.8) {Wechsel $e_1$ (Takt 2)};")
lines.append("\\node[font=\\scriptsize,ferm,anchor=south] at (2.2,1.8) {Wechsel $e_2$ (Takt 2)};")
lines.append("\\node[font=\\scriptsize,grau,anchor=north] at (0,-2.4) {Schnitt je zweier Gevierte: der Zweier $\\{1,-1\\}$; acht Glieder, drei Gevierte, gerechnet};")
lines.append("\\end{tikzpicture}")
open(os.path.join(out,'baustein_geacht_form.tex'),'w').write("\n".join(lines)+"\n")

# ---- Fano beidseitig ----
def conj(x):
    if len(x)==1: return x.copy()
    h=len(x)//2; return np.concatenate([conj(x[:h]), -x[h:]])
def cd(x,y):
    if len(x)==1: return x*y
    h=len(x)//2; a,b,c,d=x[:h],x[h:],y[:h],y[h:]
    return np.concatenate([cd(a,c)-cd(conj(d),b), cd(d,a)+cd(b,conj(c))])
def u(i): v=np.zeros(8); v[i]=1; return v
lines_O=[]
for i,j,k in itertools.combinations(range(1,8),3):
    p=cd(u(i),u(j))
    if np.allclose(np.abs(p),u(k)): lines_O.append((i,j,k))
assert len(lines_O)==7 and all(i^j==k for i,j,k in lines_O)
blade={1:'e_1',2:'e_2',3:'e_1e_2',4:'e_3',5:'e_1e_3',6:'e_2e_3',7:'e_1e_2e_3'}
# Lage: Standard-Fano mit Punkten 1..7: Ecken 1,2,4; Mitten 3(=1^2),6(=2^4),5(=1^4); Zentrum 7
import math
P={1:(90,2.0),2:(210,2.0),4:(330,2.0)}
xy={k:(r*math.cos(math.radians(a)),r*math.sin(math.radians(a))) for k,(a,r) in P.items()}
xy[3]=tuple((np.array(xy[1])+np.array(xy[2]))/2); xy[6]=tuple((np.array(xy[2])+np.array(xy[4]))/2); xy[5]=tuple((np.array(xy[4])+np.array(xy[1]))/2); xy[7]=(0.0,0.0)
L=["% GERECHNET von erzeuge_bausteine.py — Geraden aus den Produkttripeln der Oktaven, Blade-Beschriftung aus a⊕b=c, nicht von Hand",
   "\\begin{tikzpicture}[scale=1.25,pt/.style={circle,draw,fill=white,inner sep=1pt,font=\\scriptsize,minimum size=7mm}]"]
for (i,j,k) in lines_O:
    pts=[i,j,k]
    if 7 in pts and set(pts)!={3,5,6}:
        a,b=[p for p in pts if p!=7]; L.append(f"\\draw[thick,raum] ({xy[a][0]:.3f},{xy[a][1]:.3f})--({xy[b][0]:.3f},{xy[b][1]:.3f});")
    elif set(pts)=={3,5,6}:
        r=math.dist(xy[3],(0,0)); L.append(f"\\draw[thick,ferm] (0,0) circle ({r:.3f});")
    else:
        # Seite: die beiden Ecken
        corners=[p for p in pts if p in (1,2,4)]; L.append(f"\\draw[thick,zeit] ({xy[corners[0]][0]:.3f},{xy[corners[0]][1]:.3f})--({xy[corners[1]][0]:.3f},{xy[corners[1]][1]:.3f});")
for k,(x,y) in xy.items():
    L.append(f"\\node[pt] at ({x:.3f},{y:.3f}) {{$e_{k}$}};")
    dx=0.0; dy=0.42 if y>=0 else -0.42
    if k==7: dx,dy=0.0,-0.45
    L.append(f"\\node[font=\\tiny,grau] at ({x+dx:.3f},{y+dy:.3f}) {{${blade[k]}$}};")
L.append("\\node[font=\\scriptsize,align=left,anchor=west] at (2.6,0.9) {sieben Punkte: die Einheiten $e_1\\ldots e_7$ der Oktaven,\\\\darunter in Grau dieselbe Stelle als Blade von $\\Cl(0,3)$};")
L.append("\\node[font=\\scriptsize,align=left,anchor=west] at (2.6,-0.2) {sieben Geraden (der Kreis eingeschlossen):\\\\Produkttripel $e_ie_j=\\pm e_k$ der Oktaven und zugleich\\\\Produkttripel der Blades; Regel $a\\oplus b=c$ auf beiden Seiten};")
L.append("\\end{tikzpicture}")
open(os.path.join(out,'baustein_fano_beidseitig.tex'),'w').write("\n".join(L)+"\n")
print("Bausteine geschrieben:",os.listdir(out))
