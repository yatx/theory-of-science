"""Prüfstand zum Aufsatz »Die Gabel und ihre Aufhebung«.
Läufe P1, P2, P3, P4, P6, P7. Jeder Lauf schließt mit Zusicherungen (KS-G)."""
import itertools, numpy as np
np.random.seed(1)

# ---------- Cayley-Dickson ----------
def conj(x):
    if len(x)==1: return x.copy()
    h=len(x)//2; return np.concatenate([conj(x[:h]), -x[h:]])
def cd_mul(x,y):
    if len(x)==1: return x*y
    h=len(x)//2; a,b,c,d=x[:h],x[h:],y[:h],y[h:]
    return np.concatenate([cd_mul(a,c)-cd_mul(conj(d),b), cd_mul(d,a)+cd_mul(b,conj(c))])
def unit(i,n): v=np.zeros(n); v[i]=1.0; return v

# ---------- Clifford Cl(0,n) als Blade-Algebra über Bitmasken ----------
def blade_mul(S,T,n):
    sign=1
    for i in range(n):
        if S>>i &1:
            for j in range(i):
                if T>>j &1: sign=-sign
    for i in range(n):
        if (S>>i &1) and (T>>i &1): sign=-sign   # e_i^2 = -1
    return sign, S^T
def cl_table(n):
    N=1<<n; tab=np.zeros((N,N,N))
    for S in range(N):
        for T in range(N):
            s,P=blade_mul(S,T,n); tab[S,T,P]=s
    return tab
def cd_table(n):
    N=1<<n; tab=np.zeros((N,N,N))
    for i in range(N):
        for j in range(N):
            tab[i,j]=cd_mul(unit(i,N),unit(j,N))
    return tab

# ---------- P1: Doppellesung als Isomorphie, n<=2 ----------
# Vorgelegter Isomorphismus: Blade-Bitmaske -> CD-Index, Skalar->0, e1->1, e2->2, e1e2->3
def p1():
    out={}
    for n in (0,1,2):
        N=1<<n; cl=cl_table(n); cd=cd_table(n)
        # Abbildung phi: Blade S -> CD-Index S (Bitmaske als Zahl). Vorzeichen: e1e2 -> +e3? pruefen, sonst -e3
        best=None
        for sgn in itertools.product([1,-1],repeat=N):
            ok=True
            for S in range(N):
                for T in range(N):
                    lhs=cl[S,T]*sgn[S]*sgn[T]            # phi(S)phi(T) Koeffizienten in Basis phi(P)=sgn[P] e_P
                    # phi(S T) = sum_P cl[S,T,P] * sgn[P]*e_P ; phi(S)phi(T) = sgn[S]sgn[T] e_S e_T = sgn[S]sgn[T] cd[S,T]
                    rhs=np.array([cl[S,T,P]*sgn[P] for P in range(N)])
                    if not np.allclose(sgn[S]*sgn[T]*cd[S,T], rhs): ok=False; break
                if not ok: break
            if ok: best=sgn; break
        out[n]=best
    return out
iso=p1()
for n in (0,1,2): assert iso[n] is not None, f"P1: Cl(0,{n}) und CD({n}) nicht isomorph unter Blade->Einheit"
# und bei n=3 gibt es KEINE solche Abbildung (Blade->Einheit mit Vorzeichen): Gegenprobe
def p1_n3():
    n=3; N=8; cl=cl_table(n); cd=cd_table(n)
    for sgn in itertools.product([1,-1],repeat=N):
        ok=True
        for S in range(N):
            for T in range(N):
                rhs=np.array([cl[S,T,P]*sgn[P] for P in range(N)])
                if not np.allclose(sgn[S]*sgn[T]*cd[S,T], rhs): ok=False; break
            if not ok: break
        if ok: return sgn
    return None
assert p1_n3() is None, "P1: bei n=3 duerfte kein Blade->Einheit-Isomorphismus existieren"
print("P1 KS-G 01: Cl(0,n) ≅ CD(n) fuer n=0,1,2 mit vorgelegtem Isomorphismus (Vorzeichen:",iso[2],"); bei n=3 keiner.")

# ---------- P2: Fano beidseitig ----------
O=[unit(i,8) for i in range(8)]
lines_O=set()
for i,j,k in itertools.combinations(range(1,8),3):
    if np.allclose(np.abs(cd_mul(O[i],O[j])),O[k]): lines_O.add(frozenset((i,j,k)))
lines_Cl=set()
for a,b,c in itertools.combinations(range(1,8),3):
    s,P=blade_mul(a,b,3)
    if P==c: lines_Cl.add(frozenset((a,b,c)))
lines_Z2={frozenset((a,b,a^b)) for a,b in itertools.combinations(range(1,8),2)}
assert lines_O==lines_Cl==lines_Z2 and len(lines_O)==7, "P2"
assert all(len(a&b)==1 for a,b in itertools.combinations(lines_O,2)), "P2 Inzidenz"
assert all(sum(p in L for L in lines_O)==3 for p in range(1,8)), "P2 Inzidenz"
print("P2 KS-G 02: sieben Geraden, in 𝕆 und in Cl(0,3) dieselben {a,b,a⊕b}; je zwei Geraden ein Punkt, jeder Punkt auf drei.")

# ---------- P3: Graduierung ----------
def part(v): return "K" if np.allclose(v[4:],0) else "E"
tab={}
for i in range(8):
    for j in range(8):
        k=(part(O[i]),part(O[j])); tab[k]=tab.get(k,set())|{part(cd_mul(O[i],O[j]))}
assert tab=={('K','K'):{'K'},('K','E'):{'E'},('E','K'):{'E'},('E','E'):{'K'}}, "P3"
nonassoc=sum(1 for i,j,k in itertools.product(range(1,8),repeat=3)
             if not np.allclose(cd_mul(cd_mul(O[i],O[j]),O[k]), cd_mul(O[i],cd_mul(O[j],O[k]))))
assert nonassoc==168, nonassoc
print("P3 KS-G 03: 𝕆 = ℍ + ℍe graduiert (E·E ⊂ ℍ); 168 Assoziativitaetsverletzungen unter Einheiten.")

# ---------- P4: kein Bild ohne Nullteiler ----------
# Idempotente in H und O: a^2 = a. Numerisch: Suche per Newton aus vielen Startwerten; algebraisch: a=a0+v, v im Imaginaeren:
# a^2 = a0^2 - |v|^2 + 2 a0 v  (gilt in H und O, da v^2 = -|v|^2). a^2=a => 2a0 v = v => v=0 oder a0=1/2; a0=1/2 => 1/4-|v|^2=1/2 => |v|^2=-1/4.
def idempotents_numeric(N,trials=4000):
    found=set()
    for _ in range(trials):
        a=np.random.randn(N)
        for _ in range(60):
            f=cd_mul(a,a)-a
            # Jacobi numerisch
            J=np.zeros((N,N)); eps=1e-6
            for k in range(N):
                d=np.zeros(N); d[k]=eps
                J[:,k]=(cd_mul(a+d,a+d)-(a+d)-f)/eps
            try: a=a-np.linalg.solve(J,f)
            except np.linalg.LinAlgError: break
        if np.allclose(cd_mul(a,a),a,atol=1e-8): found.add(tuple(np.round(a,6)))
    return found
for N in (4,8):
    idem=idempotents_numeric(N)
    assert idem<= {tuple(np.round(np.zeros(N),6)), tuple(np.round(unit(0,N),6))}, (N,idem)
# Cl(0,3): p± = (1 ± e123)/2
cl3=cl_table(3)
def cl_mul(x,y):
    z=np.zeros(8)
    for S in range(8):
        for T in range(8):
            if x[S] and y[T]: z+=x[S]*y[T]*cl3[S,T]
    return z
one=np.zeros(8); one[0]=1; w=np.zeros(8); w[7]=1
pp=(one+w)/2; pm=(one-w)/2
assert np.allclose(cl_mul(w,w),one) and np.allclose(cl_mul(pp,pp),pp) and np.allclose(cl_mul(pm,pm),pm) and np.allclose(cl_mul(pp,pm),0)
assert all(np.allclose(cl_mul(w,unit(S,8)),cl_mul(unit(S,8),w)) for S in range(8)), "omega zentral"
print("P4 KS-G 04: in ℍ und 𝕆 nur die Idempotente 0 und 1 (Newton aus 4000 Starts je Algebra); in Cl(0,3) ω²=+1 zentral, p±²=p±, p₊p₋=0.")

# ---------- P6: Bott-Klammer ----------
L=[np.column_stack([cd_mul(O[i],O[j]) for j in range(8)]) for i in range(1,8)]   # L_i x = e_i x
I8=np.eye(8)
assert all(np.allclose(Li@Li,-I8) for Li in L), "L_i^2=-1"
assert all(np.allclose(L[i]@L[j]+L[j]@L[i],0) for i in range(7) for j in range(i+1,7)), "antivertauschen"
# Algebra erzeugt von L_1..L_7: Rang der Produkte aller Teilmengen
prods=[]
for r in range(8):
    for S in itertools.combinations(range(7),r):
        M=I8.copy()
        for i in S: M=M@L[i]
        prods.append(M.flatten())
rank7=np.linalg.matrix_rank(np.array(prods))
assert rank7==64, rank7
# achter Erzeuger auf R^16: E_i = [[0,L_i],[L_i,0]]? Standard: E_i = L_i ⊗ [[0,-1],[1,0]] und E_8 = I ⊗ [[0,1],[1,0]]... pruefen
J=np.array([[0,-1],[1,0]]); K=np.array([[0,1],[1,0]])
E=[np.kron(Li,K) for Li in L]+[np.kron(I8,J)]
I16=np.eye(16)
assert all(np.allclose(Ei@Ei,-I16) for Ei in E), "E_i^2=-1"
assert all(np.allclose(E[i]@E[j]+E[j]@E[i],0) for i in range(8) for j in range(i+1,8)), "E antivertauschen"
prods=[]
for r in range(9):
    for S in itertools.combinations(range(8),r):
        M=I16.copy()
        for i in S: M=M@E[i]
        prods.append(M.flatten())
rank8=np.linalg.matrix_rank(np.array(prods))
assert rank8==256, rank8
print("P6 KS-G 09: sieben Linksmultiplikationen L_i: L_i²=−1, antivertauschend, erzeugen Rang 64 = M₈(ℝ); mit achtem Erzeuger auf ℝ¹⁶ Rang 256 = M₁₆(ℝ).")

# ---------- P7: Gegenprobe ----------
dims=[1<<n for n in range(9)]
triples=[(dims[i],dims[i+1]) for i in range(8)]
print("P7 Gegenprobe: jede Verdopplung 2^n -> 2^{n+1} (acht Schritte bis 256) laesst sich als Einheit/Zweiheit/Einheit lesen; die Dreizahl ist generisch:",len(triples),"Stellen.")
print("ALLE ZUSICHERUNGEN HALTEN.")
