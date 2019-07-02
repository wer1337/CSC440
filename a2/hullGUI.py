#!/usr/bin/env python3
# if using python 2, swap the next two lines
# from Tkinter import *
from tkinter import *
import copy
from convexhull import computeHull
from random import randint


def hello(event):
    print("Single Click, Button-l") 

def addPoint(event):
	drawPoint(w, event.x, event.y)
	points.append((event.x,event.y))

def drawPoint(canvas,x,y):
	# r = 4
	# id = canvas.create_oval(x-r,y-r,x+r,y+r)
	# id = canvas.create_image((x,y),image=ram,state=NORMAL)
	id = canvas.create_text((x,y,), font='Helvetica 12 normal', text=str(x) + "," + str(y), fill = 'red')
	return id

def showPoints(event):
	print(points)

def drawHull():
	points = [(191, 642), (190, 591), (181, 718), (181, 645), (166, 738), (178, 604), (161, 659), (145, 642), (118, 759), (138, 664), (107, 760), (73, 789), (85, 730), (81, 741), (37, 769), (41, 741), (172, 452), (131, 537), (131, 530), (45, 693), (84, 615), (95, 591), (52, 664), (92, 588), (21, 702), (26, 662), (135, 473), (136, 468), (43, 563), (85, 510), (22, 554), (126, 456), (51, 510), (48, 500), (97, 456), (101, 451), (166, 399), (50, 392), (52, 386), (83, 381), (70, 327), (141, 344), (106, 291), (62, 238), (126, 296), (12, 136), (53, 105), (98, 181), (79, 135), (127, 217), (60, 16), (77, 39), (83, 55), (99, 93), (120, 153), (81, 16), (165, 270), (115, 75), (160, 228), (113, 28), (122, 44), (161, 180), (136, 25), (162, 163), (180, 240)]
	# points = []
	# for i in range(randint(3,400)):
	# 	points.append((randint(10, 800), randint(10,800)))
	# list(set(points))
	# print(len(points))
	hull = copy.copy(computeHull(points))
	hull.append(hull[0])
	for i in range(0,len(hull)-1):
		x1 = hull[i][0]
		y1 = hull[i][1]
		x2 = hull[i+1][0]
		y2 = hull[i+1][1]
		w.create_line(x1, y1, x2, y2, width=3)

	print(len(points))


master = Tk()
points = []

submit_button = Button(master, text="Draw Hull", command=drawHull)
submit_button.pack()
quit_button = Button(master, text="Quit", command=master.quit)
quit_button.pack()

canvas_width = 1000
canvas_height = 800
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
ram = PhotoImage(file="ram-sm.gif")
w.pack()
w.bind('<Button-1>', addPoint)

w.mainloop()
