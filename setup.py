from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='algorithm_ranking',
    version="0.1",
    description="Methodology to rank algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/as641651/AlgorithmRanking',
    author='Aravind Sankaran',
    author_email='aravindsankaran22@gmail.com',
    packages= find_packages(), # finds packages inside current directory
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">3",

)