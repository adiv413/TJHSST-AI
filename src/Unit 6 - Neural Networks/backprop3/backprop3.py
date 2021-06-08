import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import math
import random
import time

def main():
    # setup
    # get inequality
    inequality = args[1]
    negate = False

    if ">=" in inequality:
        ineq_type = ">="
    elif ">" in inequality:
        ineq_type = ">"
    elif "<=" in inequality:
        ineq_type = "<="
        negate = True
    else:
        ineq_type = "<"
        negate = True
        
    radius = float(inequality[inequality.find(ineq_type) + len(ineq_type):])

    # get weights

    inputs = []
    expected_outputs = []

    weightfile = args[0]
    all_weights = open(weightfile, "r").read().splitlines()
    actual_weights = []

    for layer in all_weights:
        split_weights = layer.strip().split(" ")

        weights = []
        for token in split_weights:
            number = ""
            for i in token:
                if i in "-.0123456789":
                    number += i
            if number != "":
                weights.append(float(number))

        if weights == []:
            continue
        
        actual_weights.append(weights)

    initial_node_counts = [2]
    for i in range(len(actual_weights)):
        initial_node_counts.append(int(len(actual_weights[i]) / initial_node_counts[i]))

    # combine the weights

    # first layer

    new_first_weights = []
    count = 0
    while count < len(actual_weights[0]):
        new_first_weights.append(actual_weights[0][count] / math.sqrt(radius))
        new_first_weights.append(0)
        new_first_weights.append(actual_weights[0][count + 1])
        count += 2

    count = 0
    while count < len(actual_weights[0]):
        new_first_weights.append(0)
        new_first_weights.append(actual_weights[0][count] / math.sqrt(radius))
        
        new_first_weights.append(actual_weights[0][count + 1])
        count += 2

    actual_weights[0] = [i for i in new_first_weights]
    # for layer in actual_weights:
    #     print(*layer) 

    # all hidden layers

    for i in range(1, len(actual_weights) - 1):
        new_weights = []

        count = 0

        while count < len(actual_weights[i]):
            for j in range(initial_node_counts[i]):
                new_weights.append(actual_weights[i][count + j])
            for j in range(initial_node_counts[i]):
                new_weights.append(0)

            count += initial_node_counts[i]

        count = 0

        while count < len(actual_weights[i]):
            for j in range(initial_node_counts[i]):
                new_weights.append(0)
            for j in range(initial_node_counts[i]):
                new_weights.append(actual_weights[i][count + j])

            count += initial_node_counts[i]


        actual_weights[i] = [j for j in new_weights]


    # output layer
    if negate:
        actual_weights[-1] = [-actual_weights[-1][0], -actual_weights[-1][0]]
    else:
        actual_weights[-1] = [actual_weights[-1][0], actual_weights[-1][0]]

    if negate:
        actual_weights.append([math.e * (1 + math.e) / (2 * math.e)])
    else:
        actual_weights.append([(1 + math.e) / (2 * math.e)])

    node_counts = [3]
    for i in range(len(actual_weights)):
        node_counts.append(int(len(actual_weights[i]) / node_counts[i]))

    print("Layer counts:", *node_counts)
    for layer in actual_weights:
        print(*layer) 

    # n = len(inputs[0])
    # node_counts = [n, 12, 6, 1, 1]
    # weights = [[[random.random() for k in range(node_counts[i + 1])] for j in range(node_counts[i])] for i in range(len(node_counts) - 1)]

    # print("Layer counts:", *node_counts)

    # # weights go from curr layer to next layer, 3d array
    # print()
    # print()
    # for layer in weights:
    #     for length in range(len(layer[0])):
    #         for i in layer:
    #             print(i[length], end=" ")
    #     print()  

main()