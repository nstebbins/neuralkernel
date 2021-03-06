# Neuralkernel
[![Build Status](https://travis-ci.org/nstebbins/neuralkernel.svg?branch=master)](https://travis-ci.org/nstebbins/neuralkernel)
[![PyPI](https://img.shields.io/pypi/v/neuralkernel.svg)](https://pypi.python.org/pypi/neuralkernel)
[![PyPI - License](https://img.shields.io/pypi/l/neuralkernel.svg)](https://pypi.python.org/pypi/neuralkernel)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/neuralkernel.svg)](https://pypi.python.org/pypi/neuralkernel)

This project uses networks of neuron-like computational units to build a framework of computation. Specifically, it implements characteristics traditionally found in neural networks including synaptic diversity, temporal delays, and voltage spikes. It builds on the ideas proposed in the paper [STICK: Spike Time Interval Computational Kernel, A Framework for General Purpose Computation](https://arxiv.org/abs/1507.06222).

## Getting Started

To run a sample network, you can run the module.

```bash
python -m neuralkernel
```

The networks currently implemented are:

* Inverting Memory
* Logarithm
* Maximum
* Non-Inverting Memory
* Full Subtractor

For more information on each of these networks, please check out the `docs` folder.

## Running the tests

To run the unit tests, you can run the following.

```bash
pytest
```
