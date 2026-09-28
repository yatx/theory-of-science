"""Prüfstand zu »Das Vorzeichen, das den Sphären fehlt«. Läufe V1–V6 mit Zusicherungen (KS-V)."""
import itertools, cmath, os, json

# ---------- Gruppen aus zwei antivertauschenden Erzeugern, Signatur (q1,q2) = Quadrate ----------
def make_group(q1,q2):
    def mul(a,b):
        sa,Sa=a; sb,Sb=b; s=sa*sb
        if (Sa&2) and (Sb&1): s=-s                 # e2 e1 = - e1 e2
        if (Sa&1) and (Sb&1): s*=q1                # e1^2 = q1
        if (Sa&2) and (Sb&2): s*=q2                # e2^2 = q2
        return (s,Sa^Sb)
    G=[(s,S) for s in (1,-1) for S in range(4)]
    return G,mul
def order(G,mul,e,g):
    x=g;n=1
    while x!=e: x=mul(x,g); n+=1
    return n
def subgroups4(G,mul,e):
    out=[]
    for c in itertools.combinations(G,4):
        S=set(c)
        if e in S and all(mul(a,b) in S for a in S for b in S): out.append(frozenset(S))
    return out
def geviert_typen(G,mul,e):
    return sorted("U" if any(order(G,mul,e,g)==4 for g in S) else "W" for S in subgroups4(G,mul,e))
def abelian(G,mul): return all(mul(a,b)==mul(b,a) for a in G for b in G)

E=(1,0); res={}
for name,(q1,q2) in {"Cl(2,0)":(1,1),"Cl(1,1)":(1,-1),"Cl(0,2)":(-1,-1)}.items():
    G,mul=make_group(q1,q2)
    assert len({mul(a,b) for a in G for b in G})==8
    typ=geviert_typen(G,mul,E); res[name]=(typ,abelian(G,mul),sorted(order(G,mul,E,g) for g in G))
    # Quotient nach {±1}: Klassen = Bitmasken, Produkt = XOR
    cls=sorted({S for _,S in G})
    assert cls==[0,1,2,3] and all((A^B)==(B^A) for A in cls for B in cls) and all(A^A==0 for A in cls)
assert res["Cl(2,0)"][0]==["U","W","W"] and not res["Cl(2,0)"][1]
assert res["Cl(1,1)"][0]==["U","W","W"] and not res["Cl(1,1)"][1]
assert res["Cl(0,2)"][0]==["U","U","U"] and not res["Cl(0,2)"][1]
print("V1 KS-V 01: Geacht der Form je Signatur:",{k:(v[0],"abelsch" if v[1] else "nichtabelsch") for k,v in res.items()},"; Quotient nach ±1 ist stets V4 (kommutativ, alle Quadrate 1).")

# ---------- Sphären ----------
S={'S1':(0,0),'S2':(1,1),'S3':(0,1),'S4':(1,0)}   # 1 = halbzahlig; (Parität a, Parität b)
inv={v:k for k,v in S.items()}
sm=lambda x,y: inv[((S[x][0]+S[y][0])%2,(S[x][1]+S[y][1])%2)]
assert sm('S2','S3')=='S4'==sm('S3','S2') and all(sm(x,x)=='S1' for x in S) and all(sm(x,y)==sm(y,x) for x in S for y in S)
# Leitgrößen (Aufbau, Tafel der Sphären): Parität aus den Exponenten
leit={'m':(1,-2),'q':(-0.5,0.5),'psi':(0,-1.5),'qpsi':(-0.5,-1.0)}
par=lambda ab: (int(2*ab[0])%2, int(2*ab[1])%2)
assert par(leit['m'])==S['S1'] and par(leit['q'])==S['S2'] and par(leit['psi'])==S['S3'] and par(leit['qpsi'])==S['S4']
print("V2 KS-V 02: Sphären = V4 der Paritäten; S2·S3 = S3·S2 = S4, jedes Quadrat S1; Leitgrößen m,q,ψ,qψ in S1..S4.")

# ---------- Phasen i^b unter L = iT ----------
sechzehn={'hbar':(0,0),'c^-1':(1,-1),'c':(-1,1),'c^2':(-2,2),'F':(-1,-1),'L^-2':(0,-2),'P':(-2,0),'p':(-1,-3),
          'm':(1,-2),'T':(1,0),'L':(0,1),'k':(0,-1),'nu':(-1,0),'hbar/m':(-1,2),'a':(-2,1),'V':(0,3)}
assert len(set(sechzehn.values()))==16
ph=lambda b: (int(round(2*b)))%8          # Phase i^b als Vielfaches von e^{iπ/4}: 2b mod 8
klassen={}
for k,(a,b) in sechzehn.items(): klassen.setdefault(ph(b),[]).append(k)
assert sorted(klassen)== [0,2,4,6] and all(len(v)==4 for v in klassen.values())
print("V3 KS-V 03: die sechzehn Größen von S1 stehen zu je 4 auf den Phasen 1, i, −1, −i:",{ {0:'1',2:'i',4:'−1',6:'−i'}[k]:v for k,v in sorted(klassen.items())})
# alle Sphären: Phasen aller Größen T^a L^b mit a,b in ½ℤ
alle={(a/2,b/2) for a in range(-8,8) for b in range(-8,8)}
phasen={ph(b) for _,b in alle}; assert phasen==set(range(8))
halb={ph(b) for _,b in alle if (int(round(2*b)))%2==1}; ganz={ph(b) for _,b in alle if (int(round(2*b)))%2==0}
assert halb=={1,3,5,7} and ganz=={0,2,4,6}
# Z8: Untergruppen der Ordnung 4
Z8=list(range(8)); zm=lambda x,y:(x+y)%8
assert len(subgroups4(Z8,zm,0))==1
print("V4 KS-V 04: Phasen aller Größen bilden Z8; b ganz auf den vierten, b halb auf den primitiven achten Einheitswurzeln; Z8 hat genau ein Geviert (Umlauf).")
# volle Struktur (Parität a, Phase): Z2 x Z8, abelsch
G16=[(x,y) for x in range(2) for y in range(8)]; m16=lambda p,q:((p[0]+q[0])%2,(p[1]+q[1])%8)
assert all(m16(p,q)==m16(q,p) for p in G16 for q in G16)
print("V5 KS-V 05: Ladungsparität × Phase = Z2 × Z8, abelsch; nicht isomorph zum Geacht der Form (nichtabelsch).")

# ---------- Gegenprobe: alle Gruppen der Ordnung 8 ----------
def cyc(n): return list(range(n)), (lambda a,b:(a+b)%n), 0
def prod(A,B):
    GA,mA,eA=A; GB,mB,eB=B
    return [(a,b) for a in GA for b in GB], (lambda p,q:(mA(p[0],q[0]),mB(p[1],q[1]))), (eA,eB)
Z2=cyc(2); Z4=cyc(4)
gruppen={"Z8":cyc(8),"Z4xZ2":prod(Z4,Z2),"Z2xZ2xZ2":prod(prod(Z2,Z2),Z2)}
G,mul=make_group(1,1); gruppen["D4"]=(G,mul,E)
G,mul=make_group(-1,-1); gruppen["Q8"]=(G,mul,E)
zaehl={}
for name,(G,mul,e) in gruppen.items():
    sg=subgroups4(G,mul,e); typ=sorted("U" if any(order(G,mul,e,g)==4 for g in S_) else "W" for S_ in sg)
    zaehl[name]=(len(sg),"".join(typ),"abelsch" if abelian(G,mul) else "nichtabelsch")
assert zaehl["Z8"][0]==1 and zaehl["Z2xZ2xZ2"][0]==7 and zaehl["D4"][0]==3 and zaehl["Q8"][0]==3 and zaehl["Z4xZ2"][0]==3
print("V6 KS-V 06: Gevierte je Gruppe der Ordnung 8:",zaehl)
print("ALLE ZUSICHERUNGEN HALTEN.")
json.dump({"sechzehn_phasen":{str(k):v for k,v in klassen.items()},"geachte":zaehl},open(os.path.join(os.path.dirname(__file__),"ergebnis_vorzeichen.json"),"w"),indent=1)
