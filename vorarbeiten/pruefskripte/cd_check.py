import numpy as np, itertools
# Cayley-Dickson: Elemente als Arrays der Länge 2^n; Produkt (a,b)(c,d)=(ac - conj(d) b, d a + b conj(c))
def conj(x):
    if len(x)==1: return x.copy()
    h=len(x)//2; return np.concatenate([conj(x[:h]), -x[h:]])
def mul(x,y):
    if len(x)==1: return x*y
    h=len(x)//2; a,b,c,d=x[:h],x[h:],y[:h],y[h:]
    return np.concatenate([mul(a,c)-mul(conj(d),b), mul(d,a)+mul(b,conj(c))])
def e(i,n=8):
    v=np.zeros(n); v[i]=1; return v
O=[e(i) for i in range(8)]
# Assoziativität prüfen
assoc_fail=sum(1 for i,j,k in itertools.product(range(1,8),repeat=3)
               if not np.allclose(mul(mul(O[i],O[j]),O[k]), mul(O[i],mul(O[j],O[k]))))
print("Assoziativitaetsverletzungen unter Einheiten:", assoc_fail)
# Z2-Graduierung: Kern = span(e0..e3) = H, Huelle = span(e4..e7)
def part(v): return "K" if np.allclose(v[4:],0) else ("H" if np.allclose(v[:4],0) else "gemischt")
tab={}
for i in range(8):
    for j in range(8):
        tab[(part(O[i]),part(O[j]))]=tab.get((part(O[i]),part(O[j])),set())|{part(mul(O[i],O[j]))}
print("Graduierung Kern/Huelle:",tab)
# Fano: Tripel {i,j,k} imaginaerer Einheiten mit e_i e_j = +-e_k
lines=[]
for i,j,k in itertools.combinations(range(1,8),3):
    p=mul(O[i],O[j])
    if np.allclose(np.abs(p),O[k]): lines.append((i,j,k))
print("Fano-Geraden (Anzahl):",len(lines), lines)
print("Einheit liegt auf # Geraden:", {i:sum(i in L for L in lines) for i in range(1,8)})
# Jede Gerade erzeugt Unteralgebra ~ H (assoziativ)?
for L in lines:
    S=[O[0]]+[O[i] for i in L]
    ok=all(np.allclose(mul(mul(a,b),c),mul(a,mul(b,c))) for a in S for b in S for c in S)
    print(L,"assoziativ:",ok)
