#
# Modified by Wyatt Howe and Nth Party, Ltd. for
# https://github.com/nthparty/bn254 from the archive
# of the Apache Milagro Cryptographic Library found at
# https://github.com/apache/incubator-milagro-crypto.
#
# Python 3.7 Code to implement basic MPIN protocol API
# M.Scott August 2018
#

import hashlib
from bn254 import ecp
from bn254 import ecp2
from bn254 import curve
from bn254 import big
from bn254.ecp import *
from bn254.ecp2 import *
from bn254 import pair
from bn254.fp12 import *

# hash ID to point on curve


def H(mpin_id):
    r = curve.r
    p = curve.p
    h = hashlib.new(curve.SHA)
    h.update(bytes(mpin_id, 'utf-8'))
    x = big.from_bytes(h.digest())
    x %= p
    P = ECp()
    while not P.set(x):
        x = x + 1
# work out co-factor
    nb = p.bit_length()
    cf = 1
    cf = cf << (nb + 4) // 2
    cf += p
    cf //= r

    if cf != 1:
        P = cf * P

    return P


def random_generate():
    FS = curve.EFS
    s = big.rand(curve.r)
    Z = big.to_bytes(s)
    return Z


def get_server_secret(Z):
    Q = ecp2.generator()
    s = big.from_bytes(Z)
    Q = s * Q
    return Q.toBytes()


def get_client_secret(Z, ID):
    P = H(ID)
    s = big.from_bytes(Z)
    P = s * P
    return P.toBytes(False)

# subtract pin.ID from Secret key SK to create Token


def extract_pin(ID, PIN, SK):
    P = H(ID)
    P = -(PIN * P)
    S = ECp()
    if not S.fromBytes(SK):
        return bytearray(0)
    S.add(P)
    # S.affine()
    return S.toBytes(False)

# U=xH(ID)


def client_1(ID, X):
    P = H(ID)
    if X:
        w = big.from_bytes(X)
    else:
        w = big.rand(curve.r)
        X = big.to_bytes(w)
    P = w * P
    return (X, P.toBytes(False))

# reconstitute Client secret S from Token and PIN
# V=(x+y)S


def client_2(X, Y, ID, PIN, TK):
    P = H(ID)

    S = ECp()
    if not S.fromBytes(TK):
        return bytearray(0)
    x = big.from_bytes(X)
    y = big.from_bytes(Y)

    x = (x + y) % curve.r
    x = curve.r - x

    S.add(PIN * P)

    S = x * S
    return S.toBytes(False)

# authenticate


def server(ID, Y, SS, U, V):
    P = H(ID)
    y = big.from_bytes(Y)

    Q = ecp2.generator()

    P = y * P

    sQ = ECp2()
    if not sQ.fromBytes(SS):
        return (False, Fp12(), Fp12())

    TU = ECp()
    if not TU.fromBytes(U):
        return (False, bytearray(0), bytearray(0))

    TV = ECp()
    if not TV.fromBytes(V):
        return (False, bytearray(0), bytearray(0))

    TU.add(P)
    # TU.affine()

    r = pair.double_ate(Q, TV, sQ, TU)
    r = pair.fexp(r)

    if r.isone():
        return (True, bytearray(0), bytearray(0))

# failed - diagnose it
    E = r.toBytes()
    r = pair.e(Q, TU)
    F = r.toBytes()
    return (False, E, F)


MAXPIN = 10000
TS = 10
TRAP = 200


def kangaroo(E, F):
    FS = curve.EFS

    e = Fp12()
    e.fromBytes(E)
    f = Fp12()
    f.fromBytes(F)

# Pollards Kangaroos
    t = f.copy()

    distance = []
    table = []
    s = 1
    for m in range(0, TS):
        distance.append(s)
        table.append(t.copy())
        s *= 2
        t.usqr()

    t = Fp12.one()
# set trap
    dn = 0
    for j in range(0, TRAP):
        i = t.a.a.a.int() % TS
        t *= table[i]
        dn += distance[i]

# release wild kangaroo
    f = t.copy()
    f.conj()
    steps = 0
    dm = 0
    while dm - dn < MAXPIN:
        steps = steps + 1
        if steps > 4 * TRAP:
            break
        i = e.a.a.a.int() % TS
        e *= table[i]
        dm += distance[i]
        if e == t:
            res = dm - dn
            break
        if e == f:
            res = dn - dm
            break

    if steps > 4 * TRAP or dm - dn >= MAXPIN:
        res = 0
    return res


def add_G1(A, B):
    """ Add two points in G1: C = A + B """
    A1 = ECp()
    B1 = ECp()
    if not A1.fromBytes(A):
        return None
    if not B1.fromBytes(B):
        return None
    A1.add(B1)
    return A1.toBytes(False)


def add_G2(A, B):
    """ Add two points in G2: C = A + B """
    A1 = ECp2()
    B1 = ECp2()
    if not A1.fromBytes(A):
        return None
    if not B1.fromBytes(B):
        return None
    A1.add(B1)
    return A1.toBytes()
