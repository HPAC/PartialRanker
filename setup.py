from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='partial_ranker',
    version="1.0.0",
    description="Partial Ranker is a python library that implements methodologies for ranking a given set of objects that have a strict partial order relation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/HPAC/PartialRanker',
    author='Aravind Sankaran',
    author_email='aravind.sankaran@rwth-aachen.de',
    packages= find_packages(), # finds packages inside current directory
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">3.6",
    install_requires=open("requirements.txt").read().splitlines(),

)
