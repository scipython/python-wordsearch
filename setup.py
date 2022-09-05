from setuptools import setup, find_packages
from pathlib import Path

root = Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (root / "README.rst").read_text(encoding="utf-8")

setup(
    name="python-wordsearch",
    version="1.0.1",
    description="A package for creating word searches",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/scipython/python-wordsearch",
    author="Christian Hill",
    author_email="xn.hill@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Education",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    keywords="wordsearch, puzzle",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[],
    extras_require={"dev": ["black", "pytest-cov", "tox", "ipython", "sphinx"]},
    # no need for MANIFEST.in, which should be reserved only for build-time files
    project_urls={
        "Bug Reports": "https://github.com/scipython/python-wordsearch/issues",
    },
)
