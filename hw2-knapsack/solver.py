#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import attrgetter
Item = namedtuple("Item", ['index', 'value', 'weight', 'value_density'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        density = float(int(parts[0])/int(parts[1]))
        items.append(Item(i-1, int(parts[0]), int(parts[1]), density))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    # ----- default algorithm -----
    value = 0
    taken = [0]*len(items)

    # for item in items:
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight

    if item_count * capacity > 1000000000:
        # ---- Greedy algorithm (value density) ------
        value = greedy(items, capacity, taken, value)
        output_data = str(value) + ' ' + str(0) + '\n'
    else:
        # ----- Dynamic Programming -----
        value = dp_matrix(item_count, capacity, items, taken)
        output_data = str(value) + ' ' + str(1) + '\n'
    
    # prepare the solution in the specified output format
    # output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

def greedy(items, capacity, taken, value):
    weight = 0
    for item in sort_items(items, 'value_density'):
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return value

def sort_items(items, key_value):
    return sorted(items.copy(), key=attrgetter(key_value))

def dp_matrix(item_count, capacity, items, taken):
    K = [[0 for w in range(capacity + 1)] for i in range(item_count)]
    for i in range(1, item_count):
        for w in range(1, capacity + 1):
            if items[i].weight <= w:
                K[i][w] = max([K[i - 1][w - items[i].weight] + items[i].value, K[i - 1][w]])
            else:
                K[i][w] = K[i - 1][w]
    
    W = capacity
    for i in range(item_count - 1, 1, -1):
        if K[i][W] != K[i-1][W]:
            taken[i] = 1
            W = W - items[i].weight
    
    return K[item_count - 1][capacity]   

def dp(capacity, index):
    if index == 0:
        return 0
    elif items[index].weight <= capacity:
        return max(dp(capacity, index - 1), items[index].value + dp(capacity - items[index].weight, index - 1))
    else:
        return dp(capacity, index - 1)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

