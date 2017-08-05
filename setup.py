# coding: utf-8
import setuptools


setuptools.setup(
    name="nbd",
    version="0.0.1",
    author="Tony Fast",
    author_email="tony.fast@gmail.com",
    description="Documentation for notebooks.",
    license="BSD-3-Clause",
    keywords="IPython Jupyter",
    url="http://github.com/tonyfast/nbd",
    py_modules=['nbd'],
    #     long_description=read("readme.rst"),
    classifiers=[
        "Topic :: Utilities",
        "Framework :: IPython",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=[
        'nbconvert', 'entrypoints', 
    ], tests_require=[])
