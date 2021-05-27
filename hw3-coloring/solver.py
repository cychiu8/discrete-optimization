#!/usr/bin/python
# -*- coding: utf-8 -*-

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    count = 0

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # ------ constraint programming ------
    # check which node is adjecent to the other one
    nodes_map =[[] for _ in range(node_count)]
    for edge in edges:
        nodes_map[edge[0]].append(edge[1])
        nodes_map[edge[1]].append(edge[0])

    max_color = 0

    # build a trivial solution
    # every node has its own color
    solution = [None] * node_count

    # First-fail principle
    # Choose the most connected node

    # ---- first algorithm: color by the degrees of neighbors ----
    if(node_count != 250):
        for i in sort_connected_node(nodes_map):
            node = i[0]
            if(solution[node] == None):
                max_color = color_vertex(nodes_map, node, max_color, solution)

    # ---- second algorithm: while loop ----
    # colored_vertex = 0
    # next_node = []
    # next_node.append(sort_connected_node(nodes_map)[1][0])
    # while (colored_vertex < node_count):
    #     node = next_node.pop()
    #     if(solution[node] == None):
    #         max_color = color_vertex(nodes_map, node, max_color, solution)
    #         colored_vertex = colored_vertex + 1
    #         for i in nodes_map[node]:
    #             if (solution[i] == None):
    #                 next_node.append(i)

    # ---- third algorithm ----
    # next_node = []
    # for i in sort_connected_node(nodes_map):
    #     node = i[0]
    #     next_node.append(node)
    #     while next_node:
    #         this_node = next_node.pop()
    #         if(solution[this_node] == None):
    #             max_color = color_vertex(nodes_map, this_node, max_color, solution)
    #             for nei in nodes_map[this_node]:
    #                 if(solution[nei] == None):
    #                     next_node.append(nei)     

    # ---- fourth algorithm ----
    # first_node = sort_connected_node(nodes_map)[0][0]
    # g = Graph(node_count)
    # g.graph = nodes_map
    # for color_vertex in range(1, node_count):
    #     if g.graphColoring(color_vertex):
    #         continue

    # ---- fifth algorithm
    if(node_count == 250):
        notColoredMap = sortNotColoredMap(nodes_map, solution)
        emptyList = [[] for _ in range(len(solution))]
        while(not notColoredMap == emptyList):
            thisNode = notColoredMap[0][0]
            avaliableColorList = avaliableColor(thisNode, nodes_map, max_color, solution)
            for color in range(0, max_color + 1):
                if (avaliableColorList[color] == True):
                    solution[thisNode] = color
                    break
            if solution[thisNode] == None:
                max_color = max_color + 1
                solution[thisNode] = max_color
            notColoredMap = sortNotColoredMap(nodes_map, solution)

    # prepare the solution in the specified output format
    output_data = str(len(set(solution))) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def sortNotColoredMap(adjacentMap, solution):
    notColorMap = [[] for _ in range(len(solution))]
    for i in range(len(adjacentMap)):
        for node in adjacentMap[i]:
            if solution[node] == None:
                notColorMap[i].append(node)
    # print(notColorMap)
    return sort_map(notColorMap)

def avaliableColor(thisNode, adjacentMap, maxAvailableColor, solution):
    avaliableColorList = [True] *( maxAvailableColor + 1)
    for node in adjacentMap[thisNode]:
        if not solution[node] == None:
            avaliableColorList[solution[node]] = False
    return avaliableColorList

# def is_safe(n, nodes_map, solution, color):
#     for node in nodes_map[n]:
#         if(solution[node] == color):
#             return False
#     return True

# def graphColoringUtil(nodes_map, color_vertex, solution, colored_number):
#     if (colored_number == len(solution)):
#         print('color_vertex + 1 == n')
#         print(color_vertex)
#         print('=')
#         print(n)
#         return True
    
#     for c in range(1, color_vertex + 1):
#         if is_safe(n, nodes_map, solution, c):
#             print('c----')
#             print(c)
#             solution[n] = c
#             if graphColoringUtil(nodes_map, color_vertex, solution, colored_number + 1):
#                 return True
#             solution[n] = 0

def color_vertex(nodes_map, this_node, max_color, solution):
    available_color = [True] * (max_color + 1)
    for node in nodes_map[this_node]:
        if solution[node] != None:
            available_color[solution[node]] = False
    for i in range(len(available_color)):
        if (available_color[i] == True):
            solution[this_node] = i
            return max_color
    
    max_color = max_color + 1
    solution[this_node] = max_color
    
    return max_color

# def connected_node(nodes_map):
#     max_node = 0
#     for i in range(0, len(nodes_map)):
#         if(len(nodes_map[i]) > len(nodes_map[max_node])):
#             max_node = i
#     return max_node

def sort_map(nodes_map):
    return sorted(nodes_map, key=lambda x: len(x), reverse=True)

def sort_connected_node(nodes_map):
    node_connected = {}
    for i in range(len(nodes_map)):
        node_connected[i] = len(nodes_map[i])
    return sorted(node_connected.items(), key=lambda x: x[1], reverse=True)

# class Algorithm1:
#     def __init__(self, colored, available_color, nodes_map, solution):
#         self.colored = colored
#         self.available_color = available_color
#         self.nodes_map = nodes_map
#         self.solution = solution

#     def createNodes(self, edges, node_count):
#         self.nodes_map =[[] for _ in range(node_count)]
#         for edge in edges:
#             self.nodes_map[edge[0]].append(edge[1])
#             self.nodes_map[edge[1]].append(edge[0])

class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def isSafe(self, v, solution, c):
        for i in self.graph[v]:
            if solution[i] == c:
                return False
        return True

    def graphColorUtil(self, m, solution, v):
        if v == self.V:
            return True
        for c in range(1, m + 1):
            if self.isSafe(v, solution, c) == True:
                solution[v] == c
                if self.graphColorUtil(m, solution, v + 1) == True:
                    return True
                solution[v] = None

    def graphColoring(self, m):
         solution = [None] * self.V
         if self.graphColorUtil(m, solution, 0) == False:
             return False
        

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

 