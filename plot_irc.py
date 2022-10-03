#!/usr/bin/env python3

import sys
import cclib
import numpy as np


import matplotlib.pyplot as plt
import seaborn as sns


def read_data(f):
    return cclib.io.ccread(f)

def main():
    filename = sys.argv[1]

    data = read_data(filename)

    print(data)


if __name__ == '__main__':
    main()

