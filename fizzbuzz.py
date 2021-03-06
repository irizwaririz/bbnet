"""
FizzBuzz is the following problem:
For each of the numbers 1 to 100:
* if the number is divisible by 3, print "fizz"
* if the number is divisible by 5, print "buzz"
* if the number is divisible by 15, print "fizzbuzz"
* otherwise, just print the number
"""
from typing import List

import numpy as np

from bbnet.train import train
from bbnet.nn import NeuralNet
from bbnet.layers import Linear, Tanh
from bbnet.optimizers import GD

from bbnet.data import Batch, Stochastic, MiniBatchStochastic

def fizz_buzz_encode(x: int) -> List[int]:
    if x % 15 == 0:
        return [0, 0, 0, 1] # fizzbuzz
    elif x % 5 == 0:
        return [0, 0, 1, 0] # buzz
    elif x % 3 == 0:
        return [0, 1, 0, 0] # fizz
    else:
        return [1, 0, 0, 0] # x


def binary_encode(x: int) -> List[int]:
    """
    10 digit binary encoding of x
    """
    return [x >> i & 1 for i in range(10)]

inputs = np.array([
    binary_encode(x)
    for x in range(101, 1024)
])

targets = np.array([
    fizz_buzz_encode(x)
    for x in range(101, 1024)
])

net = NeuralNet([
    Linear(input_size=10, output_size=50),
    Tanh(),
    Linear(input_size=50, output_size=4)
])

train(net=net,
      inputs=inputs,
      targets=targets,
      num_epochs=5000,
      optimizer=GD(lr=0.01),
      iterator=Stochastic())

for x in range(1, 101):
    prediction = net.forward(binary_encode(x)) # [0.2324 0.25252 0.9999 0.2424252]
    prediction_idx = np.argmax(prediction) # 2
    actual_idx = np.argmax(fizz_buzz_encode(x)) # [0 0 1 0] -> 2
    labels = [str(x), "fizz", "buzz", "fizzbuzz"]
    print(x, labels[prediction_idx], labels[actual_idx])