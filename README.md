# AlgorithmRanking:

A methodology to rank algorithms. In order to run the code, use one of the following methods:

## 1) Manual Installation

### Requirements:

1. numpy
2. pandas
2. matplotlib


Clone this directory and execute the following command inside the directory

```bash
pip install .
```

## 2) Use Docker

### Requirements:

1. Docker

Clone this directory and execute the following command inside the directory

Build image:

```bash
docker build -t [IMAGE_NAME] .
```
Map the ports for jupyter noteboon and the current working directory to the container, and Run the image

```bash
 docker run -it -p 0.0.0.0:8005:8888 -v ${1:-$PWD}:/home/user [IMAGE_NAME]
```
The jupyter notebook runs on port 8005

Run Jupyter notebook (inside the container). 

```bash
jupyter-notebook --ip=0.0.0.0 --allow-root
```

## Usage

Refer the ```.ipynb``` files [here](/examples/simulated)
