from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='partial_ranker',
    version="0.2",
    description="Algorithms to rank objects with ties based on measurements data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/HPAC/PartialRanker',
    author='Aravind Sankaran',
    author_email='aravind.sankaran@rwth-aachen.de',
    packages= find_packages(), # finds packages inside current directory
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">3",

)
