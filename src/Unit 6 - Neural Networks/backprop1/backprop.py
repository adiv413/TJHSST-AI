import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import math
import random
import time

def main():
    # setup

    input_file = open(args[0], "r").read().splitlines()

    raw_transfer_function = "logistic"
    transfer_function_map = {"linear" : linear, "relu" : relu, "logistic" : logistic, "scaled_logistic" : scaled_logistic}
    transfer_function = transfer_function_map[raw_transfer_function.lower()]
    transfer_function_dx = logistic_dx

    alpha = 0.1 # learning rate
    epochs = 50000

    inputs = []
    expected_outputs = []

    for line in input_file:
        split_line = [i.strip() for i in line.split("=>")]
        inputs.append([int(i) for i in (split_line[0] + " 1").split(" ")])
        expected_outputs.append([int(i) for i in split_line[1].split(" ")])

    n = len(inputs[0])
    node_counts = [n, 2, 1, 1]
    weights = [[[random.random() for k in range(node_counts[i + 1])] for j in range(node_counts[i])] for i in range(len(node_counts) - 1)]
    
    print("Layer counts:", *node_counts)

    # run forward and backprop

    for current_epoch in range(epochs):
        for current_input_idx in range(len(inputs)):
            inp_list = inputs[current_input_idx]
            # print(inp_list)
            x_values = [[0.0 for j in range(node_counts[i])] for i in range(len(node_counts))] # node values for all nodes in the network

            for i in range(len(x_values[0])):
                x_values[0][i] = inp_list[i]

            forward_prop(x_values, weights, transfer_function)
            # print(x_values[-1])
            # print()
            # print(inp, expected_outputs)
            backprop(x_values, weights, transfer_function_dx, expected_outputs[current_input_idx], alpha)

            if current_epoch > epochs - 6:
                print(expected_outputs[current_input_idx], x_values[-1])

        if current_epoch % int(epochs / 10) == 0:
            for layer in weights:
                for length in range(len(layer[0])):
                    for node in layer:
                        print(node[length], end=" ")
                print()
            

    # weights go from curr layer to next layer, 3d array
    # print(inputs)
    # print(expected_outputs)
    # print(x_values)
    # print(weights)
    print()
    print()
    for layer in weights:
        for length in range(len(layer[0])):
            for i in layer:
                print(i[length], end=" ")
        print()  

def backprop(x_values, weights, transfer_function_dx, expected_outputs, alpha):
    errors = [[0.0 for j in range(len(x_values[i]))] for i in range(len(x_values))] # initialize errors to empty list with same shape as x_values
    gradients = [[[0.0 for k in j] for j in i] for i in weights] # stores negative gradient * alpha values, same shape as weights
    
    # print("gradients", gradients)
    # print()
    # print("x vals", x_values)
    # print()
    # print("weights", weights)
    # print()
    # print("expected", expected_outputs)

    for layer in range(len(x_values) - 2, -1, -1): # layer
        for i in range(len(x_values[layer])): # each node in layer
            if layer == len(x_values) - 2: # if this is the last layer: special case
                first_neg_gradient = (expected_outputs[i] - x_values[layer + 1][i]) * x_values[layer][i]

                # print(expected_outputs[i], x_values[layer + 1][i])
                # print("t, x * w, x", expected_outputs[i], x_values[layer + 1][i], x_values[layer][i])
                # print("first gradient", first_neg_gradient)

                errors[layer][i] = (expected_outputs[i] - x_values[layer + 1][i]) * weights[layer][i][0] * transfer_function_dx(x_values[layer][i])
                gradients[layer][i][0] = alpha * first_neg_gradient # negative gradient for the very last weight 

                # print("first error", errors[layer][i])
                # print("first weight", weights[layer][i][0])
            else:
                # compute error first, then the negative gradient
                sum_errors = 0.0

                for j in range(len(errors[layer + 1])): # iterate through all of the errors in the next layer

                    # print(len(weights), len(x_values), len(errors), layer, i, j)
                    # print(weights[layer])
                    # print(x_values[layer - 1])
                    # print(x_values[layer])
                    # print(x_values[layer + 1])
                    # print(errors[layer - 1])
                    # print(errors[layer])
                    # print(errors[layer + 1])
                    
                    sum_errors += weights[layer][i][j] * errors[layer + 1][j]
                    neg_gradient = x_values[layer][i] * errors[layer + 1][j]
                    # print("gradient", layer, i, j, neg_gradient)
                    gradients[layer][i][j] = alpha * neg_gradient

                # print("sum errors", layer, i, j, sum_errors)
                # print()
                errors[layer][i] = sum_errors * transfer_function_dx(x_values[layer][i])

    for layer in range(len(gradients)):
        for i in range(len(gradients[layer])):
            for j in range(len(gradients[layer][i])): # update all weights with the respective negative gradient * alpha value
                weights[layer][i][j] += gradients[layer][i][j]

    # print("weights", weights)

    # print("errors", errors)
    # time.sleep(1)
    # print()

def forward_prop(x_values, weights, transfer_function):
    for layer in range(len(x_values) - 1): # layer = index of current layer
        # print(layer)
        curr_layer = x_values[layer]
        curr_weights = weights[layer]
        next_layer = [0.0 for layer in x_values[layer + 1]] # used to accumulate all of the node * weight values

        # outer: next layer, inner: curr layer
        if layer != len(x_values) - 2: # if we're not at the last layer
            for i in range(len(curr_layer)):
                for j in range(len(next_layer)):
                    curr_weight = curr_weights[i][j]
                    next_layer[j] += float(curr_layer[i] * curr_weight)
            
            for i in range(len(next_layer)):
                next_layer[i] = float(transfer_function(next_layer[i]))

        else:
            assert(len(curr_layer) == len(curr_weights) and len(curr_weights[0]) == 1)
            next_layer = [curr_layer[i] * curr_weights[i][0] for i in range(len(curr_weights))]

        for i in range(len(next_layer)): # set the next layer of x_values
            x_values[layer + 1][i] = next_layer[i]

def linear(inp):
    return inp

def relu(inp):
    return inp if inp > 0 else 0

def logistic(inp):
    try:
        return 1 / (1 + math.e ** (-inp))
    except Exception as e:
        if inp > 0:
            return 1
        return 0


def scaled_logistic(inp):
    return 2 * logistic(inp) - 1

def logistic_dx(inp):
    # temp = logistic(inp)
    return inp * (1 - inp)

main()