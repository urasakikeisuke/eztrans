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
VERSION = "1.2"
PYTHON_REQUIRES = ">=3.6"
INSTALL_REQUIRES = [
    "fire==0.4.0",
    "webdriver-manager==3.5.2",
    "selenium==3.141.0",
    "googletrans==4.0.0-rc1",
    "pyperclip==1.8.2",
]
PACKAGES = setuptools.find_packages()
CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

ENTRY_POINTS = {
    "console_scripts": [
        "ez-deepl = eztrans.deepl:main",
        "ez-google = eztrans.google:main",
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
