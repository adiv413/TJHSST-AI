import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import math

def main():
    weightfile = args[0]
    all_weights = open(weightfile, "r").read().splitlines()
    
    transfer_function_map = {"t1" : t1, "t2" : t2, "t3" : t3, "t4" : t4}
    transfer_function = transfer_function_map[args[1].lower()]

    curr_inputs = [float(i) for i in args[2:]]
    actual_weights = []
    prev_layer_len = len(curr_inputs)
    x_values = [curr_inputs]
    count = 0

    for layer in all_weights:
        actual_weights.append([])
        # print(layer)
        weights = [float(i) for i in layer.strip().split(" ")]
        next_layer = [0.0 for i in range(int(len(weights) / len(curr_inputs)))]
        
        for i in range(len(curr_inputs)):
            curr_layer = []
            for j in range(len(next_layer)):
                curr_layer.append(weights[j * len(curr_inputs) + i])
            actual_weights[count].append(curr_layer)

        if layer == all_weights[-1]:
            assert(len(curr_inputs) == len(weights))
            next_layer = [curr_inputs[i] * weights[i] for i in range(len(weights))]

        x_values.append([0.0 for i in next_layer])

        curr_inputs = next_layer

        count += 1

    forward_prop(x_values, actual_weights, transfer_function)
    print(*[round(i, 4) for i in x_values[-1]])

def forward_prop(x_values, weights, transfer_function):
    for i in range(len(x_values) - 1): # i = index of current layer
        # print(layer)
        curr_layer = x_values[i]
        curr_weights = weights[i]
        next_layer = [0.0 for i in x_values[i + 1]] # used to accumulate all of the node * weight values

        # outer: next layer, inner: curr layer
        if i != len(x_values) - 2: # if we're not at the last layer
            for j in range(len(curr_layer)):
                for k in range(len(next_layer)):
                    curr_weight = curr_weights[j][k]
                    next_layer[k] += float(curr_layer[j] * curr_weight)
            
            for j in range(len(next_layer)):
                next_layer[j] = float(transfer_function(next_layer[j]))

        else:
            assert(len(curr_layer) == len(curr_weights) and len(curr_weights[0]) == 1)
            next_layer = [curr_layer[j] * curr_weights[j][0] for j in range(len(curr_weights))]

        for j in range(len(next_layer)): # set the next layer of x_values
            x_values[i + 1][j] = next_layer[j]

def t1(inp):
    return inp

def t2(inp):
    return inp if inp > 0 else 0

def t3(inp):
    return 1 / (1 + math.e ** (-inp))

def t4(inp):
    return 2 * t3(inp) - 1

main()