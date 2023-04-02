"""setup.py"""

import setuptools  # type: ignore

with open("README.md", "r") as f:
    long_description = f.read()

DESCRIPTION = "CLI based translation tool."
NAME = 'eztrans'
AUTHOR = 'Urasaki Keisuke'
AUTHOR_EMAIL = 'urasakikeisuke.ml@gmail.com'
URL = 'http://git-docker.tasakilab:5051/git/urasaki/eztrans.git'
LICENSE = 'MIT License'
DOWNLOAD_URL = 'http://git-docker.tasakilab:5051/git/urasaki/eztrans.git'
VERSION = "3.0"
PYTHON_REQUIRES = ">=3.8"
INSTALL_REQUIRES = [
    "numpy",
    "deepl==1.14.0",
    "googletrans==4.0.0-rc1",
    "autocorrect==2.6.1",
    "pyperclip==1.8.2",
    "rich>=13.3.3",
]
PACKAGES = setuptools.find_packages()
CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3 :: Only',
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
ENTRY_POINTS = {
    "console_scripts": [
        "ez-deepl = eztrans.deepl:entory_point",
        "ez-google = eztrans.google:entory_point",
        "ez-spellcheck = ezspellcheck.spellchecker:entory_point",
    ]
}

setuptools.setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    license=LICENSE,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    entry_points=ENTRY_POINTS,
)
