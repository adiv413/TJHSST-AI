import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import random
import math

def main():
    avg_degree = float(args[0])
    method_to_make_network = args[1][0].upper()
    num_nodes = int(args[2])
    num_edges = avg_degree * num_nodes
    network = {i : set() for i in range(num_nodes)}
    curr_num_edges = 0

    if method_to_make_network == 'C':
        while curr_num_edges < num_edges:
            node1, node2 = random.sample(range(num_nodes), 2)

            if node2 not in network[node1]:
                network[node1].add(node2)
                network[node2].add(node1)
                curr_num_edges += 2

    else:
        network = {0 : set()}
        node_weights = [0] # chances of being added = (node_num_edges + 1)/total_num_edges

        for i in range(1, num_nodes):
            # pair of nodes = edges / 2
            # iteration = node
            # num_edges_remaining x 1 pair of nodes/2 edges x 1/num_iterations_remaining = x pair of nodes/num_iterations_remaining =
            # avg number of pairs of nodes that need to be added every iteration = number of random.choice() calls per iteration = 
            # ((total_edges - curr_edges)/2)/(num_nodes - len(network))

            num_pairs_of_nodes_remaining = round((num_edges - curr_num_edges) / 2)
            num_iterations_remaining = num_nodes - len(network)

            avg_num_nodes_to_add_per_iteration = min(len(network), math.ceil(num_pairs_of_nodes_remaining / num_iterations_remaining))
            network[i] = set()
            nodes_to_add = set()

            for j in range(avg_num_nodes_to_add_per_iteration):
                node = node_weights[random.randint(0, len(node_weights) - 1)]

                while node in nodes_to_add:
                    node = node_weights[random.randint(0, len(node_weights) - 1)]

                nodes_to_add.add(node)
                
            
            # nodes_to_add = random.sample(node_weights, k=avg_num_nodes_to_add_per_iteration)

            # if len(set(nodes_to_add)) != len(nodes_to_add):
            #     print('s')

            # print(len(network) - 1, math.ceil(num_pairs_of_nodes_remaining / num_iterations_remaining), nodes_to_add, i)
            
            for j in nodes_to_add:
                network[i].add(j)
                network[j].add(i)

                node_weights.append(i)
                node_weights.append(j)
                
                curr_num_edges += 2

            # print(network)

    max_degree = max([len(network[i]) for i in network])
    degree_map = {i : 0 for i in range(max_degree + 1)}

    for i in network:
        degree_map[len(network[i])] += 1

    for i in degree_map:
        if degree_map[i] != 0:
            print(str(i) + ':' + str(degree_map[i]), end=' ')
    print()

    print(get_avg_degree(network))

def get_avg_degree(network):
    total = 0.0
    for i in network:
        total += len(network[i])

    return total / len(network)

def get_nodes_to_add(network, nodes_to_add):
    node1 = get_max_node(network, len(network), nodes_to_add)

    nodes_to_add.remove(node1)
    
    node2 = get_max_node(network, len(network), nodes_to_add)

    nodes_to_add.add(node1)

    return node1, node2


def get_max_node(network, actual_size, nodes_to_add):
    nodes_to_add_list = [i for i in nodes_to_add]

    node_popularities = [abs(len(network[i]) - 2) + 1 for i in nodes_to_add_list]
    idx = random.choices(nodes_to_add_list, weights=node_popularities, k=1)[0]
    
    return idx

main()