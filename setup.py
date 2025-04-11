#!/usr/bin/env python3
from setuptools import setup

setup(
    name="quickmark",
    version="0.1.0",
    description="A simple directory bookmarking tool",
    author="wyntred",
    author_email="wyntred13@gmail.com",
    py_modules=["quickmark"],
    entry_points={
        "console_scripts": [
            "quickmark=quickmark:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)