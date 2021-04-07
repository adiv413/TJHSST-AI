import sys; args = sys.argv[1:]
import random
import math
import time

def main():
    tau = 200
    delta_t = 1
    bump = .005
    threshold = 0.95
    r = delta_t / tau # r = 0.005

    fireflies = [random.random() for i in range(5)]

    while True:
        for idx in range(len(fireflies)):
            i = fireflies[idx]

            if i >= threshold:
                fireflies[idx] = 0

                rest = [j for j in range(len(fireflies)) if j != idx]

                for idx2 in rest:
                    fireflies[idx2] += bump
                    # print('\nbump')
                    # print(actual_val[0])
                    # print(actual_val[0])
                    # print(fireflies)
                    # print()
            else:

                # FORMULA: Fce^(-t/tau)
                # where c = 1 - e^(-timestep/tau)

                fireflies[idx] += (1 - fireflies[idx]) * r

        print(fireflies)
        # time.sleep(.00001)

main()

