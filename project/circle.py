import matplotlib.pyplot as plt
import numpy as np
import math
import random

#----------------------------------------------------------------Cricle
def line_crosses_circle(x1, y1, x2, y2, r):
    dx = x2 - x1
    dy = y2 - y1
    
    a = dx**2 + dy**2
    b = 2 * (x1 * dx + y1 * dy)
    c = x1**2 + y1**2 - r**2
    
    discriminant = b**2 - 4 * a * c
    
    if discriminant < 0:
        return False
    
    sqrt_disc = math.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2 * a)
    t2 = (-b + sqrt_disc) / (2 * a)
    
    return (0 <= t1 <= 1) or (0 <= t2 <= 1)

def draw_connected_points_and_check_circles(list_of_points):

    i = 0
    for points in list_of_points:
        x_coords, y_coords = zip(*points)

        plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='C{}'.format(i), label='Path')
        i = i + 1
    
    for i in range(1, 21):
        radius = i * math.sqrt(2) / 20
        circle = plt.Circle((0, 0), radius, color='r', fill=False, linestyle='--')
        plt.gca().add_artist(circle)

    plt.xlim(-0.1, 1.5)
    plt.ylim(-0.2, 1.1)
    

    plt.gca().set_aspect('equal', adjustable='box')

    cross = []
    for points in list_of_points:
        circle_crossings = [0] * 20
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            
            for j in range(1, 21):
                radius = j * math.sqrt(2) / 20
                if line_crosses_circle(x1, y1, x2, y2, radius):
                    circle_crossings[j-1] = 1
        cross.append(circle_crossings)

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Connected 2D Points with Concentric Circles')
    plt.grid(True)

    plt.show()
    
    for v in cross:
        print(v)
    return cross


#-------------------------------------------------------------------------------
def extreme(listOfLists):
    [x_min, y_min] = listOfLists[0][0]
    [x_max, y_max] = listOfLists[-1][-1]
    for li in listOfLists:
        for p in li:
            if p[0] < x_min:
                x_min = p[0]
            if p[1] < y_min:
                y_min = p[1]
            if p[0] > x_max:
                x_max = p[0]
            if p[1] > y_max:
                y_max = p[1]
    return [x_min, y_min], [x_max, y_max]

def transfer_rescale(listOfLists):
    A, B = extreme(listOfLists)
    x_l = (1.1*(B[0]- A[0]))
    y_l = (1.1*(B[1]- A[1]))
    ep_x = 0*(1 - (B[0]- A[0])/(x_l))/1.1
    ep_y = 0*(1 - (B[1]- A[1])/(y_l))/1.1
    mainL = []
    for i in range(len(listOfLists)):
        tempL = []
        for j in range(len(listOfLists[i])):
            tempL.append([ep_x + (listOfLists[i][j][0] - A[0])/x_l, ep_y + (listOfLists[i][j][1] - A[1])/y_l])
        mainL.append(tempL)
    return mainL





# this function generates bunch of trajectories
def generate_random_2d_points(num_lists=5, max_length=20):
    list_of_points = []
    
    for _ in range(num_lists):
        list_length = random.randint(2, max_length)
        
        points = [(random.randint(1, 360), random.randint(1, 360)) for _ in range(list_length)]
        
        list_of_points.append(points)
    
    return list_of_points

# I wrote the following to rotate trajectories
def myrot(B, deg):
    rad = math.radians(deg)
    x = B[0]
    y = B[1]
    X = x*math.cos(rad) - y*math.sin(rad)
    Y = x*math.sin(rad) + y*math.cos(rad)
    return [X,Y]

def rotAll(BB, deg):
    CC = []
    for B in BB:
        CC.append(myrot(B, deg))
    return CC






#D = generate_random_2d_points(num_lists=5, max_length=5)


#D = [[[1,2], [3,6], [-1,-1], [-2, 3], [0,0]], [[11,22], [-3,16], [1,-10], [-2, 31], [45,0]], [[100, 100], [-100, -100]]]   

D = [[[0, 0], [3, 0], [4, 1]], [[1, 3.5], [4, 3.5], [5, 4.5]]]



D_rescle = transfer_rescale(D)
DD = [rotAll(D, 12) for D in D_rescle]
#DD += [rotAll(D, 5) for D in D_rescle]
#DD += [rotAll(D, 10) for D in D_rescle]
#DD += [rotAll(D, -10) for D in D_rescle]
#DD += [rotAll(D, 20) for D in D_rescle]
#draw_connected_points_and_check_radials(D_rescle)

DD += D_rescle
draw_connected_points_and_check_circles(DD)
