from tkinter import *
from cmath import *
import sys
import time

try:
    size = int(input("Size of display (pixels) (default 800): "))
except:
    size = 800

try:
    step = int(input("Number of points per unit (default 25): "))
except:
    step = 25

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

escape_times = [5, 10, 20, 35, 50, 75, 100, 200, 500]
escape_time_cols = {
    0:"#fff",
    1:"#eee",
    2:"#ddd",
    3:"#ccc",
    4:"#bbb",
    5:"#aaa",
    6:"#999",
    7:"#888",
    8:"#777",
    9:"#666",
    10:"#555",
    11:"#444",
    }

cycle_cols[n_cycle+1] = "#000"
font_size = 10

try:
    cols = int(input("Coloring (0 = none, 1 = cycles, 2 = escape time): "))
except:
    cols = 0

if cols not in [0, 1, 2]:
    cols = 0

try:
    upd_ = int(input("Update while rendering (0 = no, 1 = yes): "))
except:
    upd_ = 0

if upd_ not in [0, 1]:
    upd_ = 0

zoom = 1
cam_x = 0
cam_y = 0

tk = Tk()
cv = Canvas(tk, width=size, height=size)
cv.pack()
tk.update()

def mand(c, n, x_init=0):
    x = x_init
    if x != None:
        for i in range(n):
            x = x*x + c
            if abs(x) > 2:
                return None
    else:
        return None
    return x

def render(upd=False):
    cv.delete("all")
    if cols == 2:
        using_times = escape_times
        for i in using_times:
            if i == iters:
                using_times.pop(using_times.index(i))
        using_times.append(iters)
    for x__ in range(-2*step, 2*step):
        x = x__/(step*zoom)+cam_x
        for y__ in range(-2*step, 2*step):
            y = y__/(step*zoom)-cam_y
            c = x + y*1j
            x_ = ((x__/step)+2)*step_size*step
            y_ = ((y__/step)+2)*step_size*step
            if cols == 1:
                vals = [mand(c, iters-n_cycle)]
                if vals != [None]:
                    for i in range(n_cycle):
                        vals.append(z(c,vals[-1]))
            elif cols == 2:
                vals = [mand(c, using_times[0])]
                for i in range(1, len(using_times)):
                    incr = using_times[i]-using_times[i-1]
                    vals.append(mand(c, incr, vals[-1]))
            else:
                vals = [mand(c, iters-n_cycle)]
            cycle = n_cycle+1
            if vals[-1] != None:
                if cols == 1: # cycle coloring
                    for i in range(1, len(vals)):
                        if cycle > n_cycle:
                            val = vals[i]
                            if abs(vals[0]-val) < loop_thresh:
                                cycle = i
                    color = cycle_cols[cycle]
                else:
                    color = "#000"
            else:
                if cols == 2:
                    color = escape_time_cols[vals.index(None)]
                else:
                    color = "#fff"
            cv.create_rectangle(x_, y_, x_ + step_size, y_ + step_size, fill=color, outline="")
        if upd:        
            tk.update()
    if cols == 1:
        for i in range(1,n_cycle+1):
            cv.create_text(5, (font_size+2)*i+(5-font_size), anchor="nw", text=str(i)+"-cycle", fill=cycle_cols[i], font=("Small Fonts", font_size, "bold"))
        i += 1
        cv.create_text(5, (font_size+2)*i+(5-font_size), anchor="nw", text="Higher order cycle", fill=cycle_cols[i], font=("Small Fonts", font_size, "bold"))
    cv.create_text(size-5, 5, anchor="ne", text=str(cam_x)+"+"+str(cam_y)+"i", fill="#666", font=("Small Fonts", font_size, "bold"))
    cv.create_text(size-5, 7+font_size, anchor="ne", text="Zoom: 2^"+str(int(abs(log(zoom,2)))), fill="#666", font=("Small Fonts", font_size, "bold"))
    tk.update()


t1 = time.perf_counter()

render(True)

print("Done! :D")

t2 = time.perf_counter()
print(t2-t1)

def z_in(event=None):
    global zoom
    zoom *= 2

def z_out(event=None):
    global zoom
    zoom /= 2

def c_left(event=None):
    global cam_x
    cam_x -= 2/zoom

def c_right(event=None):
    global cam_x
    cam_x += 2/zoom

def c_up(event=None):
    global cam_y
    cam_y += 2/zoom

def c_down(event=None):
    global cam_y
    cam_y -= 2/zoom

def home(event=None):
    global cam_x
    global cam_y
    global zoom
    cam_y = 0
    cam_x = 0
    zoom = 1
    refresh()

def refresh(event=None):
    print("Refreshing...")
    render(True)
    print("Done!")

tk.bind("c", z_in)
tk.bind("z", z_out)
tk.bind("a", c_left)
tk.bind("d", c_right)
tk.bind("w", c_up)
tk.bind("s", c_down)
tk.bind("h", home)
tk.bind("r", refresh)

while True:
    tk.update()
