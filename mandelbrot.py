from tkinter import *
from cmath import *
import sys
import time

try:
    size = int(input("Size of display (pixels) (default 800): "))
except:
    size = 800

try:
    step = int(input("Number of points per unit (default 100): "))
except:
    step = 100

n_steps = 4*step
step_size = size/n_steps

try:
    iters = int(input("Number of iterations (default 1000): "))
except:
    iters = 1000

sys.setrecursionlimit(max(1024, iters))

n_cycle = 16
loop_thresh = 0.01
cycle_cols = {
    1:"#00f",
    2:"#f00",
    3:"#0f0",
    4:"#0ff",
    5:"#ff0",
    6:"#f60",
    7:"#0f6",
    8:"#60f",
    9:"#006",
    10:"#600",
    11:"#060",
    12:"#066",
    13:"#660",
    14:"#630",
    15:"#063",
    16:"#306",
    }

cycle_cols[n_cycle+1] = "#000"
font_size = 10

try:
    cols = int(input("Coloring (0 = none, 1 = cycles): "))
except:
    cols = 0

if cols not in [0, 1]:
    cols = 0

zoom = 8
cam_x = -0.5
cam_y = -0.5

_i = sqrt(-1)

tk = Tk()
cv = Canvas(tk, width=size, height=size)
cv.pack()
tk.update()

def z(c, x):
    if x != None:
        n = x*x + c
        if abs(n) < 2:
            return n
    else:
        return None

def mand(c, n):
    if n > 0:
        return z(c, mand(c, n-1))
    else:
        return z(c, 0)

t1 = time.perf_counter()

def render():
    for x__ in range(-2*step, 2*step):
        x = x__/(step*zoom)+cam_x
        for y__ in range(-2*step, 2*step):
            y = y__/(step*zoom)-cam_y
            c = x + y*_i
            x_ = ((x__/step)+2)*step_size*step
            y_ = ((y__/step)+2)*step_size*step
            vals = [mand(c, iters-n_cycle)]
            if cols == 1:
                if vals != [None]:
                    for i in range(n_cycle):
                        vals.append(z(c,vals[-1]))
            if vals[-1] == None:
                vals = [10]
            cycle = n_cycle+1
            if abs(vals[-1]) < 2:
                if cols == 1: # cycle coloring
                    for i in range(1, len(vals)):
                        if cycle > n_cycle:
                            val = vals[i]
                            if abs(vals[0]-val) < loop_thresh:
                                cycle = i
                    color = cycle_cols[cycle]
                if cols == 0:
                    color = "#000"
            else:
                color = "#fff"
            cv.create_rectangle(x_, y_, x_ + step_size, y_ + step_size, fill=color, outline="")
        tk.update()

render()

if cols == 1:
    for i in range(1,n_cycle+1):
        cv.create_text(5, (font_size+2)*i+(5-font_size), anchor="nw", text=str(i)+"-cycle", fill=cycle_cols[i], font=("Small Fonts", font_size, "bold"))
    i += 1
    cv.create_text(5, (font_size+2)*i+(5-font_size), anchor="nw", text="Higher order cycle", fill=cycle_cols[i], font=("Small Fonts", font_size, "bold"))

tk.update()

print("Done! :D")

t2 = time.perf_counter()
print(t2-t1)

while True:
    tk.update()
