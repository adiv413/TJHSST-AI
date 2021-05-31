import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import math
import random
import time

def main():
    # setup
    inequality = args[0]
    ineq_type = None

    if ">=" in inequality:
        ineq_type = ">="
    elif ">" in inequality:
        ineq_type = ">"
    elif "<=" in inequality:
        ineq_type = "<="
    else:
        ineq_type = "<"
        
    radius = float(inequality[inequality.find(ineq_type) + len(ineq_type):])

    num_samples = 5000

    raw_transfer_function = "logistic"
    transfer_function_map = {"linear" : linear, "relu" : relu, "logistic" : logistic, "scaled_logistic" : scaled_logistic}
    transfer_function = transfer_function_map[raw_transfer_function.lower()]
    transfer_function_dx = logistic_dx

    alpha = 0.1 # learning rate
    epochs = 100

    inputs = []
    expected_outputs = []

    # create training pairs

    for i in range(num_samples):
        x = (random.random() - 0.5) * 3
        y = (random.random() - 0.5) * 3
        inputs.append([x, y, 1])
        output = None

        if ineq_type == ">":
            output = (x * x + y * y > radius)
        elif ineq_type == ">=":
            output = (x * x + y * y >= radius)
        elif ineq_type == "<":
            output = (x * x + y * y < radius)
        else:
            output = (x * x + y * y <= radius)

        expected_outputs.append([1 if output else 0])

    n = len(inputs[0])
    node_counts = [n, 12, 6, 1, 1]
    weights = [[[random.random() for k in range(node_counts[i + 1])] for j in range(node_counts[i])] for i in range(len(node_counts) - 1)]
    # print(inputs)
    # print(expected_outputs)
    # print(inequality)
    # print(ineq_type)
    # print(radius)
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

            # if current_epoch > epochs - 6:
            #     print(expected_outputs[current_input_idx], x_values[-1])

            # if current_epoch % int(epochs / 10) == 0:
            #     print(expected_outputs[current_input_idx], x_values[-1])

        if current_epoch % int(epochs / 10) == 0:
            for layer in weights:
                for length in range(len(layer[0])):
                    for node in layer:
                        print(node[length], end=" ")
                print()
            

    # weights go from curr layer to next layer, 3d array
    print()
    print()
    for layer in weights:
        for length in range(len(layer[0])):
            for i in layer:
                print(i[length], end=" ")
        print()  


    # test the network

    # test_inputs = []
    # test_expected_outputs = []
    # goof_count = 0
    # num_test = 500

    # for i in range(num_test):
    #     x = (random.random() - 0.5) * 3
    #     y = (random.random() - 0.5) * 3
    #     test_inputs.append([x, y, 1])
    #     output = None

    #     if ineq_type == ">":
    #         output = (x * x + y * y > radius)
    #     elif ineq_type == ">=":
    #         output = (x * x + y * y >= radius)
    #     elif ineq_type == "<":
    #         output = (x * x + y * y < radius)
    #     else:
    #         output = (x * x + y * y <= radius)

    #     test_expected_outputs.append([1 if output else 0])

    # for idx in range(len(test_inputs)):
    #     inp_list = test_inputs[idx]
    #     x_values = [[0.0 for j in range(node_counts[i])] for i in range(len(node_counts))] # node values for all nodes in the network

    #     for i in range(len(x_values[0])):
    #         x_values[0][i] = inp_list[i]

    #     forward_prop(x_values, weights, transfer_function)
    #     print(x_values[-1], test_expected_outputs[idx])
    #     val = 1 if x_values[-1][0] > 0.5 else 0

    #     if val != test_expected_outputs[idx][0]:
    #         goof_count += 1

    # print(goof_count, goof_count/num_test)


def backprop(x_values, weights, transfer_function_dx, expected_outputs, alpha):
    errors = [[0.0 for j in range(len(x_values[i]))] for i in range(len(x_values))] # initialize errors to empty list with same shape as x_values
    gradients = [[[0.0 for k in j] for j in i] for i in weights] # stores negative gradient * alpha values, same shape as weights

    for layer in range(len(x_values) - 2, -1, -1): # layer
        for i in range(len(x_values[layer])): # each node in layer
            if layer == len(x_values) - 2: # if this is the last layer: special case
                first_neg_gradient = (expected_outputs[i] - x_values[layer + 1][i]) * x_values[layer][i]
                errors[layer][i] = (expected_outputs[i] - x_values[layer + 1][i]) * weights[layer][i][0] * transfer_function_dx(x_values[layer][i])
                gradients[layer][i][0] = alpha * first_neg_gradient # negative gradient for the very last weight 
            else:
                # compute error first, then the negative gradient
                sum_errors = 0.0

                for j in range(len(errors[layer + 1])): # iterate through all of the errors in the next layer
                    sum_errors += weights[layer][i][j] * errors[layer + 1][j]
                    neg_gradient = x_values[layer][i] * errors[layer + 1][j]
                    gradients[layer][i][j] = alpha * neg_gradient

                errors[layer][i] = sum_errors * transfer_function_dx(x_values[layer][i])

    for layer in range(len(gradients)):
        for i in range(len(gradients[layer])):
            for j in range(len(gradients[layer][i])): # update all weights with the respective negative gradient * alpha value
                weights[layer][i][j] += gradients[layer][i][j]

def forward_prop(x_values, weights, transfer_function):
    for layer in range(len(x_values) - 1): # layer = index of current layer
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
    return inp * (1 - inp)

main()