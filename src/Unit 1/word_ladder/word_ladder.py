# Aditya Vasantharao, pd. 4
# Create and analyze a "word ladder" made out of a list of words
# Usage: python word_ladder.py [word_list_file]

# @param word_list_file: .txt file containing the list of 6 letter words to be made into a graph
# A sample file (words.txt) is provided in this folder

import sys
import time

args = sys.argv[1:]

def main():
    start = time.time()
    words = open(args[0], 'r').read().splitlines()
    graph = {}
    groups = {}

    for i in words:
        graph[i] = set()

        for j in range(6):
            same_letters = i[0:j] + ' ' + i[j + 1:]
            
            if same_letters not in groups:
                groups[same_letters] = set()
            
            groups[same_letters].add(i)

    for key, val in groups.items(): # this is actually faster than dict[key] bc items() is implemented in c bc library function
        if len(val) > 1:
            nodes = list(val)

            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    graph[nodes[i]].add(nodes[j])
                    graph[nodes[j]].add(nodes[i])
    
    total = 0
    highest_degree = 0
    degree_map = {}
    degree_list_str = ''

    for i in graph:
        degree = len(graph[i])
        total += degree

        if degree > highest_degree:
            highest_degree = degree
        
        if degree not in degree_map:
            degree_map[degree] = 1
        else:
            degree_map[degree] += 1

    for i in range(highest_degree + 1):
        if i not in degree_map:
            degree_list_str += '0 '
        else:
            degree_list_str += str(degree_map[i]) + ' '
    
    degree_list_str = degree_list_str[:-1] # get rid of extra space

    end = time.time()
    elapsed = end - start

    print('Word count: ' + str(len(words)))
    print('Edge count: ' + str(total // 2))
    print('Degree list: ' + degree_list_str)
    print('Construction time: ' + str(elapsed)[:4] + 's')

    if(len(args) > 1):
        first = args[1]
        second = args[2]

        second_highest_degree_word = ''

        if highest_degree - 1 not in degree_map:
            for i in graph:
                if len(graph[i]) == highest_degree:
                    second_highest_degree_word = i
                    break
        else:
            for i in graph:
                if len(graph[i]) == highest_degree - 1:
                    second_highest_degree_word = i
                    break

        print('Second degree word: ' + second_highest_degree_word)

        component_sizes, largest_comp_size, k2_count, k3_count, k4_count = connectedComponents(graph)

        print('Connected component size count: ' + str(component_sizes))
        print('Largest component size: ' + str(largest_comp_size))
        print('K2 count: ' + str(k2_count))
        print('K3 count: ' + str(k3_count))
        print('K4 count: ' + str(k4_count))
        
        print('Neighbors: ', end='')
        print(*graph[first])

        print('Farthest: ' + farthestWord(first, graph))
        print('Path: ' + shortestPath(first, second, graph))

def shortestPath(first, second, graph):
    queue = [first]
    visited = {first : ''}

    while queue:
        curr = queue.pop()

        if curr == second:
            ret = ''
            node = second

            while node != '':
                ret = node + ' ' + ret
                node = visited[node]

            return ret

        toVisit = graph[curr] - set(visited.keys())
        queue = list(toVisit) + queue

        for i in toVisit:
            visited[i] = curr

    return ''


def farthestWord(first, graph):
    queue = [first]
    visited = set(first)
    farthest = ''

    while queue:
        curr = queue.pop()
        farthest = curr

        toVisit = graph[curr] - visited
        queue = list(toVisit) + queue

        for i in toVisit:
            visited.add(i)

    return farthest

def connectedComponents(graph):
    visited_nodes = set()

    current_comp = {}
    component_sizes = set()
    largest_comp_size = 0
    k2_count = 0
    k3_count = 0
    k4_count = 0

    while len(visited_nodes) < len(graph):
        remaining = set(graph.keys()) - visited_nodes

        for first in remaining: # for whatever reason this is the fastest way to get a random element from a set
            break

        queue = [first] 

        while queue: # fill the current connected component until it's full, analyze it after
            curr = queue.pop()
            visited_nodes.add(curr) # we can't revisit the current node
            current_comp[curr] = graph[curr]

            toVisit = graph[curr] - visited_nodes
            queue = list(toVisit) + queue

        # analyze current_comp
        num_nodes = len(current_comp)
        largest_comp_size = max(num_nodes, largest_comp_size)
        component_sizes.add(num_nodes)

        if num_nodes == 2:
            k2_count += 1
            
        elif num_nodes == 3:
            edge_count = sum([len(current_comp[i]) for i in current_comp])

            if edge_count == 6:
                k3_count += 1

        elif num_nodes == 4:
            edge_count = sum([len(current_comp[i]) for i in current_comp])

            if edge_count == 12:
                k4_count += 1
                        

        # reset vars
        current_comp = {}

    return (len(component_sizes), largest_comp_size, k2_count, k3_count, k4_count)

main()