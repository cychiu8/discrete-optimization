#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
import random
import logging
from collections import namedtuple

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

Point = namedtuple("Point", ['x', 'y'])

initialTemperature = 100
lowestTemperature =  1e-7
# change the temperature when rejecting the new status for this limit number
limitReject = 150
iteration = 500


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    logging.info('=== start to solve ===')

    # parse the input
    lines = input_data.split('\n')

    # the number of cities needed to visist
    nodeCount = int(lines[0])
    logging.debug('number of cities:' + str(nodeCount))

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # calulate the distance matrix
    matrix = distMatrix(points, nodeCount)

    # build a trivial solution (initial solution)
    solution = initialSolution(matrix)       

    obj = calculateLength(points, nodeCount, solution)
    bestSolution = solution
    bestObj = obj
    
    currentTemperature = initialTemperature
    while (currentTemperature > lowestTemperature):
        countForReject = 0
        countForIteration = 0
        while(countForReject < limitReject and countForIteration < iteration):

            # search neighbors
            neighborSolution = searchNeighbors(solution)
            neighborObj = calculateLength(points, nodeCount, neighborSolution)

            # the delta between neighbor and current
            delta = neighborObj - obj

            # the probability threshod
            threshold = np.random.rand()

            # calculate the exponential function
            expValue = np.exp(-delta / currentTemperature)

            # whether to accept this neighbor
            if delta < 0 or expValue > threshold:
                solution = neighborSolution
                obj = neighborObj
                if obj < bestObj:
                    bestObj = obj
                    bestSolution = solution
                    logging.debug('update best solution obj:' + str(bestObj))
            else:
                countForReject = countForReject + 1
            
            countForIteration = countForIteration + 1
        currentTemperature = 0.99 * currentTemperature

    return prepareOutput(bestObj, bestSolution)


def prepareOutput(obj, solution):
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def distMatrix(points, nodeCount):
    matrix = [[0 for i in range(nodeCount)] for i in range(nodeCount)]
    for i in range(nodeCount):
        for j in range(i+1, nodeCount):
            matrix[i][j] = length(points[i], points[j])
            matrix[j][i] = matrix[i][j]
    return matrix


def searchNeighbors(solution):
    neighborStrategy = np.random.randint(3)
    if neighborStrategy == 0:
        neighborSolution = swap(solution)
    elif neighborStrategy == 1:
        neighborSolution = reverse(solution)
    else:
        neighborSolution = transpose(solution)
    return neighborSolution


def swap(solution):
    i, j = np.random.randint(0, len(solution) - 1, 2)
    if i >= j:
        i, j = j, i + 1
    solution[i], solution[j] = solution[j], solution[i]
    return solution


def reverse(solution):
    i, j = np.random.randint(0, len(solution) - 1, 2)
    if i >= j:
        i, j = j, i + 1
    solution[i:j] = solution[i:j][::-1]
    return solution


def transpose(solution):
    i, j, k = sorted(np.random.randint(0, len(solution) - 2, 3))
    j += 1
    k += 2
    slice1, slice2, slice3, slice4 = solution[:i], solution[i:j], solution[j:k], solution[k:]
    solution = slice1 + slice3 + slice2 + slice4
    return solution


def twoOpt(solution, nodeCount, matrix, temperature):
    i = random.randint(0, nodeCount - 2)
    j = i
    while(j == i):
        j = random.randint(0, nodeCount - 2)

    change = matrix[solution[i]][solution[j]] + matrix[solution[i+1]][solution[j+1]
                                                                      ] - matrix[solution[i]][solution[i+1]] - matrix[solution[j]][solution[j+1]]
    if(change < 0):
        # print('small: swap')
        return swapTwo(solution, i, j)
    else:
        threshold = random.uniform(0, 1)
        if math.exp((-1)*change/temperature) > threshold:
            # print("change: "+ str(change) + " temp: " + str(temperature) + " prob:" + str(math.exp((-1)*change/temperature))+ " threshold:" + str(threshold) )
            return swapTwo(solution, i, j)
        else:
            return solution


def swapTwo(solution, i, j):
    tmp = solution[i+1]
    solution[i+1] = solution[j]
    solution[j] = tmp
    return solution


def minChange(solution, nodeCount, matrix):
    minchange = 0
    mini = 0
    minj = 0
    for i in range(0, nodeCount-3):
        for j in range(i+2, nodeCount-1):
            change = matrix[solution[i]][solution[j]] + matrix[solution[i+1]][solution[j+1]
                                                                              ] - matrix[solution[i]][solution[i+1]] - matrix[solution[j]][solution[j+1]]
            # print("i:" + str(i) + " j:" + str(j) + " change:" + str(change) + " minchange:" + str(minchange))
            if minchange > change:
                # print(" change:" + str(change) + " minchange:" + str(minchange))
                minchange = change
                mini = i
                minj = j
                # print('mini: ' + str(mini) + ' minj:' + str(minj))
    if(mini != minj):
        # print("----")
        # print('mini: ' + str(mini) + ' minj:' + str(minj))
        # print(solution)
        tmp = solution[mini+1]
        solution[mini+1] = solution[minj]
        solution[minj] = tmp
        # print(solution)
    return solution


def initialSolution(matrix):
    numCitiest = len(matrix)
    solution = []

    # depends on the number of cities
    if numCitiest > 1890:
        # visit the nodes in the order they appear in the file
        solution = list(range(0, numCitiest))
        return solution

    # nearest neighborhood
    # the cities thats is not in solution now
    togo = list(range(numCitiest))

    first = togo.pop(0)
    solution.append(first)

    for i in range(numCitiest - 1):
        minLength = sys.maxsize
        minj = solution[i]
        for j in togo:
            if matrix[solution[i]][j] < minLength:
                minLength = matrix[solution[i]][j]
                minj = j
        solution.append(minj)
        togo.remove(minj)
    return solution

def calculateLength(points, nodeCount, solution):
    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
