from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

keywords = [
    "amino",
    "aminoapps",
    "amino.fix",
    "amino.light",
    "amino.ligt.py",
    "AminoLightPy",
    "amino-bot",
    "narvii",
    "medialab",
    "api",
    "python",
    "python3",
    "python3.x",
    "minori",
    "august",
    "augustlight",
    "aminolightpy",
    "amino.py"
]

setup(
    name="amino.light.py",
    version="0.1.7",
    url="https://github.com/AugustLigh/AminoLightPy",
    license="MIT",
    description="Best Amino.py alternative",
    author="AugustLight",
    packages=find_packages(),
    install_requires=["requests", "websocket-client"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=keywords,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)