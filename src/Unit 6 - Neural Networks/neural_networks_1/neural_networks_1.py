import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import math

def main():
    weightfile = args[0]
    all_weights = open(weightfile, "r").read().splitlines()
    
    transfer_function_map = {"t1" : t1, "t2" : t2, "t3" : t3, "t4" : t4}
    transfer_function = transfer_function_map[args[1].lower()]

    curr_inputs = [float(i) for i in args[2:]]

    for layer in all_weights:
        # print(layer)
        weights = [float(i) for i in layer.strip().split(" ")]
        next_layer = [0.0 for i in range(int(len(weights) / len(curr_inputs)))]

        # outer: next layer, inner: curr layer
        if layer != all_weights[-1]:
            for i in range(len(next_layer)):
                for j in range(len(curr_inputs)):
                    curr_weight = weights[i * len(curr_inputs) + j]
                    next_layer[i] += float(curr_inputs[j] * curr_weight)
                    

            
            for i in range(len(next_layer)):
                next_layer[i] = float(transfer_function(next_layer[i]))

        else:
            assert(len(curr_inputs) == len(weights))
            next_layer = [curr_inputs[i] * weights[i] for i in range(len(weights))]

        curr_inputs = next_layer

    print(*[round(i, 4) for i in curr_inputs])



def t1(inp):
    return inp

def t2(inp):
    return inp if inp > 0 else 0

def t3(inp):
    return 1 / (1 + math.e ** (-inp))

def t4(inp):
    return 2 * t3(inp) - 1

main()