#
# Modified by Wyatt Howe and Nth Party, Ltd. for
# https://github.com/nthparty/bn254 from the archive
# of the Apache Milagro Cryptographic Library found at
# https://github.com/apache/incubator-milagro-crypto.
#
# Python 3.7 Code to implement basic BLS protocol API
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

# hash message m to curve point

def BLS_H(m):
    h = hashlib.shake_256()
    h.update(bytes(m, 'utf-8'))
    hm=big.from_bytes(h.digest(curve.EFS))
    HM=ECp()
    while not HM.set(hm):
        hm = hm + 1
    return HM 

# generate key pair, private key SK, public key PK

def KeyPairGenerate():
    G=ecp2.generator()
    s = big.rand(curve.r)
    W=s*G
    SK = big.to_bytes(s)
    PK = W.toBytes()
    return (SK,PK)

# Sign message m using private key SK to return signature

def sign(m,SK):
    HM=BLS_H(m)
    s=big.from_bytes(SK)
    D=s*HM
    return D.toBytes(True)

# Verify signature given message m, the signature SIG, and the public key W 

def verify(SIG,m,W):
    HM=BLS_H(m)
    G=ecp2.generator()
    D=ECp()
    D.fromBytes(SIG)
    PK=ECp2()
    PK.fromBytes(W)
    D=-D

# Use new multi-pairing mechanism 
    r=pair.initmp()
    pair.another(r,G,D)
    pair.another(r,PK,HM)
    v=pair.miller(r)

#.. or alternatively
#    v = pair.double_ate(G, D, PK, HM)
    
    v = pair.fexp(v)
    if v.isone():
        return True
    return False
