#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])
    temperature = 15000

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    matrix = distMatrix(points, nodeCount)
    # build a trivial solution (initial solution)


    # print(matrix)
    print("nodeCount=" +str(nodeCount))

    if nodeCount > 1890:
        solution = range(nodeCount)
        obj = calculateLength(points, nodeCount, solution)
        # prepare the solution in the specified output format
        output_data = '%.2f' % obj + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, solution))

        return output_data

        # visit the nodes in the order they appear in the file
    solution = initialSolution(nodeCount,matrix)

    bestSolution = solution
    bestObj = calculateLength(points, nodeCount, bestSolution)

    # calculate the length of the tour
    count = 0
    while(count < 1000):
        # random
        # obj = calculateLength(points, nodeCount, solution)
        # solution = twoOpt(solution, nodeCount, points, obj)
        # print(count)


        # if(nodeCount < 201):
        #     # minchang
        #     solution = minChange(solution, nodeCount, matrix)
        #     currentLength = calculateLength(points, nodeCount, solution)
        # elif (nodeCount < 1890):
        # simulated annealing
        if count % 10 == 0:
            temperature = temperature * 0.8 
        solution = twoOpt(solution, nodeCount, matrix, temperature)
        currentLength = calculateLength(points, nodeCount, solution)

        if currentLength < bestObj:
            bestSolution = solution
            bestObj = calculateLength(points, nodeCount, bestSolution)


        # print('--- best:' +str(bestObj))

        count +=1



    # prepare the solution in the specified output format
    output_data = '%.2f' % bestObj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, bestSolution))

    return output_data

def distMatrix(points, nodeCount):
    matrix = [[0 for i in range(nodeCount)] for i in range(nodeCount)]
    for i in range(nodeCount):
        for j in range(i+1, nodeCount):
            matrix[i][j] = length(points[i], points[j])
            matrix[j][i] = matrix[i][j]
    return matrix

def twoOpt(solution, nodeCount, matrix, temperature):
    i = random.randint(0, nodeCount - 2)
    j = i
    while(j==i):
        j = random.randint(0, nodeCount - 2)

    change = matrix[solution[i]][solution[j]] + matrix[solution[i+1]][solution[j+1]] - matrix[solution[i]][solution[i+1]] - matrix[solution[j]][solution[j+1]]
    if(change < 0):
        # print('small: swap')
        return swapTwo(solution, i, j)
    else:
        threshold= random.uniform(0, 1)
        if math.exp((-1)*change/temperature) > threshold:
            # print("change: "+ str(change) + " temp: " + str(temperature) + " prob:" + str(math.exp((-1)*change/temperature))+ " threshold:" + str(threshold) )
            return swapTwo(solution, i, j)
        else:
            return solution


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
            change = matrix[solution[i]][solution[j]] + matrix[solution[i+1]][solution[j+1]] - matrix[solution[i]][solution[i+1]] - matrix[solution[j]][solution[j+1]]
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

def initialSolution(nodeCount, matrix):
    solution = []
    togo = list(range(nodeCount))
    # print("togo: " + str(togo))
    first = togo.pop(0)
    solution.append(first)
    # print("solution: "+ str(solution))
    for i in range(nodeCount - 1):
        # print("-----")
        solution[i]
        minLength = sys.maxsize
        minj = solution[i]
        for j in togo:
            if matrix[solution[i]][j] < minLength:
                minLength = matrix[solution[i]][j]
                minj = j
                # print("j: " + str(j) + " minj:" + str(minj))
        solution.append(minj)
        togo.remove(minj)
    return solution

    return list(range(0, nodeCount))

# calculate the length of the tour
def calculateLength(points, nodeCount, solution):
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

