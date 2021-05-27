#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import seed
from random import randint
import sys

def solve_it(input_data):
    seed(1)
    # return a positive integer, as a string
    return str(randint(0, sys.maxsize))

if __name__ == '__main__':
    print('This script submits the integer: %s\n' % solve_it(''))

