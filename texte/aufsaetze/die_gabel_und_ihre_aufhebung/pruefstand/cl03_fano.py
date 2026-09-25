import itertools, numpy as np
# Cl(0,3): Basisblaetter als Bitmasken; Produkt e_S e_T = sign * e_{S xor T}
def blade_mul(S,T):
    sign=1
    # Vorzeichen durch Antivertauschungen: fuer jedes Bit i in S, zaehle Bits j<i in T -> Vertauschungen
    for i in range(3):
        if S>>i &1:
            for j in range(i):
                if T>>j &1: sign=-sign
    # Quadrate e_i^2=-1 fuer gemeinsame Bits
    for i in range(3):
        if (S>>i &1) and (T>>i &1): sign=-sign
    return sign, S^T
blades=[1,2,4,3,5,6,7]  # e1,e2,e3,e12,e13,e23,e123
lines_cl=set()
for a,b,c in itertools.combinations(blades,3):
    s,p=blade_mul(a,b)
    if p==c: lines_cl.add(frozenset((a,b,c)))
print("Cl(0,3): Tripel mit e_a e_b = +-e_c:",len(lines_cl))
# (Z2)^3-Geraden: {a,b,a^b}
lines_z2={frozenset((a,b,a^b)) for a,b in itertools.combinations(range(1,8),2)}
print("(Z2)^3-Geraden:",len(lines_z2),"identisch mit Cl(0,3)-Tripeln:",lines_cl==lines_z2)
# Oktonionen-Geraden aus cd_check (Indizes 1..7): pruefe Isomorphie zu Fano via Inzidenz (jede 2 Geraden 1 Punkt, jeder Punkt 3 Geraden)
O_lines=[(1,2,3),(1,4,5),(1,6,7),(2,4,6),(2,5,7),(3,4,7),(3,5,6)]
def check(lines):
    lines=[set(l) for l in lines]
    ok1=all(len(a&b)==1 for a,b in itertools.combinations(lines,2))
    ok2=all(sum(p in l for l in lines)==3 for p in range(1,8))
    return ok1,ok2
print("Oktonionen-Tripel: je zwei Geraden ein Punkt / jeder Punkt auf drei:",check(O_lines))
print("Cl(0,3)-Tripel:  je zwei Geraden ein Punkt / jeder Punkt auf drei:",check([tuple(l) for l in lines_cl]))
# Isomorphie: Cl-Geraden sind {a,b,a xor b}; Oktonionen-Geraden ebenfalls unter Labelling e_i -> i? Pruefen:
print("Oktonionen-Geraden erfuellen a^b=c unter Index-Labelling:",all(a^b==c for a,b,c in O_lines))
