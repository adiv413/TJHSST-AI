import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import random
import math
import time
import tkinter as tk 

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def get_scaled_hex_val(charge, threshold):
    return round(min(255, (charge / threshold) * 255))

def main():
    start = time.time()
    n = int(args[0]) # 30
    r = float(args[1]) # 0.005
    bump = float(args[2]) # 0.005
    threshold = float(args[3]) # 0.95
    radius = 10

    root = tk.Tk()
    root.title("Fireflies")
    root.bind("x", lambda e: root.destroy())
    
    canvas = tk.Canvas(root, width=500, height=500, bd=0, highlightthickness=0)
    canvas.pack()

    fireflies = [random.random() for i in range(n)]
    fireflies_tk = []

    for i in fireflies:
        x = random.randint(0, 490)
        y = random.randint(0, 490)
        circle = canvas.create_oval(x, y, x + radius, y + radius, fill=rgb2hex(0, 0, 0))
        fireflies_tk.append(circle)


    while True:
        canvas.update()

        for idx in range(len(fireflies)):
            fireflies[idx] += (1 - fireflies[idx]) * r
            hex_val = get_scaled_hex_val(fireflies[idx], threshold)
            canvas.itemconfig(fireflies_tk[idx], fill=rgb2hex(hex_val, hex_val, 0))

        to_bump = [idx for idx in range(len(fireflies)) if fireflies[idx] >= threshold]
        count = 0

        # while there are still fireflies over the threshold

        while count < len(to_bump):
            curr_idx = to_bump[count]

            # bump the rest of the fireflies

            for idx in range(len(fireflies)):
                if idx not in to_bump:
                    fireflies[idx] += bump

                    hex_val = get_scaled_hex_val(fireflies[idx], threshold)
                    canvas.itemconfig(fireflies_tk[idx], fill=rgb2hex(hex_val, hex_val, 0))

                    if fireflies[idx] >= threshold:
                        to_bump.append(idx)

            fireflies[curr_idx] = 0
            canvas.itemconfig(fireflies_tk[curr_idx], fill=rgb2hex(0, 0, 0))

            count += 1

        time.sleep(0.001)

main()

