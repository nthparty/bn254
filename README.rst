=====
bn254
=====

Pure-Python library that implements operations over the BN(2,254) pairing-friendly curve.

Usage Examples
--------------
This library is available as a `package on PyPI <https://pypi.org/project/bn254>`__. Usage examples are provided below:

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

Acknowledgments
---------------
This product includes software developed at the `Apache Software Foundation <http://www.apache.org/>`__. See file headers for notices. You may find archives of the original `Apache Milagro Cryptographic Library <https://milagro.apache.org/>`__ documentation and source files (some of which were included in a modified form within this library) at the links below:

* https://milagro.apache.org/docs/
* https://apache.googlesource.com/incubator-milagro-crypto/+/70e3a/version3/python
* https://github.com/apache/incubator-milagro-crypto/tree/master/version3/python

The authors also acknowledge learning about the original Apache Milagro Cryptographic Library via the use of its source code within the `MIRACL Core Cryptographic Library <https://github.com/miracl/core>`__.
