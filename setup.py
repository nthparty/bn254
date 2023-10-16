"""
Setup, package, and build file for the bn254 cryptography library.
"""
from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

name = "bn254"
version = "0.1.2"

setup(
    name=name,
    version=version,
    packages=[name,],
    install_requires=[],
    license="Apache License 2.0",
    url="https://github.com/nthparty/bn254",
    author="Wyatt Howe",
    author_email="wyatt@nthparty.com",
    description="Pure-Python library that implements operations " + \
                "over the BN(2,254) pairing-friendly curve.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
