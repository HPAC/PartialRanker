# Partial Ranker

**Version: 1.0**

Partial Ranker is a library that implements methodologies for ranking a given set of objects that have a *strict partial order* relation. The full documentation can be found [here](https://hpac.github.io/PartialRanker/).

**Input**:

At the moment, we support only vector objects as input. An example for a set of vector objects would be:

```
objects = {
    't0' : [0.1, 0.12, 0.11, 0.13 ],
    't1' : [0.10, 0.13, 0.10 ],
    't2' : [0.32, 0.31, 0.38, 0.32, 0.37, 0.32 ],
    ...
}
```
The *better-than relation* between a pair of objects with which the partial order is formed is implemented in the library. At the moment, we support better-than relation based on comparisons of the Inter-Quantile-Intervals of the objects.

**Output**:

The output is an *ordered set partition* of the objects into ranks. For example:

```
Rank 0: ['t0', 't1'],
Rank 1: ['t2']
```

## Installation

Partial Ranker requires Python>=3.6 and can be installed using the command:

```bash
pip install git+https://github.com/HPAC/PartialRanker
```
## Examples

Details on the usage and application examples can be found [here](https://hpac.github.io/PartialRanker/notebooks-usage/01U_Usage.html). For a hands-on experience, please follow the jupyter notebooks under the folder ``examples/``.

## Cite

More details on partial ranking, the methodologies and applications can be found in [this paper](https://arxiv.org/abs/2405.18259). If you are using this library, please cite:

```
@article{sankaran2024ranking,
  title={Ranking with Ties based on Noisy Performance Data},
  author={Sankaran, Aravind and Karlsson, Lars and Bientinesi, Paolo},
  journal={arXiv preprint arXiv:2405.18259},
  year={2024}
}
```

## Acknowledgement

Financial support from the Deutsche Forschungsgemeinschaft (German Research Foundation) through grants GSC 111 and IRTG 2379 is gratefully acknowledged.