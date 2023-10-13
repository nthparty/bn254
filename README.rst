=====
bn254
=====

Pure-Python library that implements operations over the BN(2,254) pairing-friendly curve.

.. code:: python

    from bn254.curve import r as scalar_upper_bound
    from bn254.ecp import generator as base_point
    from bn254.ecp2 import generator as random_point
    from bn254.big import invmodp, rand
    from bn254.pair import e

    P = random_point()
    G = base_point()
    s = rand(scalar_upper_bound)
    t = rand(scalar_upper_bound)
    s_inv = invmodp(s, scalar_upper_bound)
    b = s_inv * t

    assert(
        e(t*P, G) == e(s*P, b*G)
    )
