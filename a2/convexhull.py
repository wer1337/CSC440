import math
import sys
import collections

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''


def yint(p1, p2, x, y3, y4):
    x1, y1 = p1
    x2, y2 = p2
    x3 = x
    x4 = x
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / \
         float((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / \
         float((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    return (px, py)


'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c. 
Note that this area will be negative 
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''


def triangleArea(a, b, c):
    return (a[0] * b[1] - a[1] * b[0] + a[1] * c[0] \
            - a[0] * c[1] + b[0] * c[1] - c[0] * b[1]) / 2.0;


'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''


def cw(a, b, c):
    return triangleArea(a, b, c) < -EPSILON;


'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''


def ccw(a, b, c):
    return triangleArea(a, b, c) > EPSILON;


'''
Given three points a,b,c,
returns True if and only if 
a,b,c are collinear
(subject to floating-point precision)
'''


def collinear(a, b, c):
    return abs(triangleArea(a, b, c)) <= EPSILON


'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''


def clockwiseSort(points):
    # get mean x coord, mean y coord
    xavg = sum(p[0] for p in points) / len(points)
    yavg = sum(p[1] for p in points) / len(points)
    angle = lambda p: ((math.atan2(p[1] - yavg, p[0] - xavg) + 2 * math.pi) % (2 * math.pi))
    points.sort(key=angle)


'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm

points is a list of (x,y) values.
So when we return points this will make it draw from point to point in the list
and connect tht least one with the first one

points = [(0,1)] x[0], x[1]
'''


def computeHull(points):
    if len(points) < 100:
        print(points)
    clockwiseSort(points)
    # stops recursion and starts to create the convex hull of the base
    if len(points) <= 3:
        return points

    # Find the midpoint
    highest = max(points, key=lambda point: point[0])
    lowest = min(points, key=lambda point: point[0])

    midpoint = (highest[0] + lowest[0]) / 2

    # splitting the points
    left_half = []
    right_half = []

    for i in points:
        if i[0] < midpoint:
            left_half.append(i)
        else:
            right_half.append(i)

    left_copy = computeHull(left_half)
    right_copy = computeHull(right_half)

    # points = merge1(left_copy, right_copy, midpoint, highest, lowest)
    points = merge(left_copy, right_copy, midpoint)
    clockwiseSort(points)
    return points


'''
Merge will be merging both left half and right half after it gets called in computeHULL
'''


def merge(left, right, midpoint):
    # Right most point of left hull
    lh_right = max(left, key=lambda point: point[0])
    # Left most point of right hull
    rh_left = min(right, key=lambda point: point[0])

    # Collections
    left_hull = left
    right_hull = right

    points = left_hull + right_hull

    # Gets the index of the left hull right most
    lh_index = left_hull.index(lh_right)
    # Gets the index of the right hull left most
    rh_index = right.index(rh_left)

    # Puts the rightmost point on the left hull at the end of the list
    left_hull = left[lh_index + 1:] + left[:lh_index + 1]
    # Puts the leftmost point on the right hull at the beginning of the list
    right_hull = right[rh_index:] + right[:rh_index]

    # Puts the rightmost point on the left hull at the beginning of the list
    left_hull_copy = left[lh_index:] + left[:lh_index]
    # Puts the leftmost point on the right hull at the end of the list
    right_hull_copy = right[rh_index + 1:] + right[:rh_index + 1]

    urh_point = rh_left
    ulh_point = lh_right
    lrh_point = urh_point
    llh_point = ulh_point

    print(left_hull_copy)
    while True:
        outlier = False

        # UPPER HULL RIGHT
        for i in range(right_hull.index(urh_point), len(right_hull)):
            if i < len(right_hull) - 1:
                if cw(ulh_point, urh_point, right_hull[i + 1]):
                    urh_point = right_hull[i + 1]
                else:
                    break

        # UPPER HULL LEFT
        for i in range(left_hull.index(ulh_point), 0, - 1):
            if i > 0:
                if cw(ulh_point, urh_point, left_hull[i - 1]):
                    ulh_point = left_hull[i - 1]
                else:
                    break

        # LOWER HULL RIGHT
        for i in range(right_hull_copy.index(lrh_point), 0, - 1):
            if i > 0:
                if ccw(llh_point, lrh_point, right_hull_copy[i - 1]):
                    lrh_point = right_hull_copy[i - 1]
                else:
                    break

        # LOWER HULL LEFT
        for i in range(left_hull_copy.index(llh_point), len(left_hull_copy)):
            if i < len(left_hull_copy) - 1:
                if ccw(llh_point, lrh_point, left_hull_copy[i + 1]):
                    llh_point = left_hull_copy[i + 1]
                else:
                    break

        # If there is another index following and
        # If the intersect of yint @ midpoint is greater than or equal to the following points
        #
        if (right_hull.index(urh_point) != len(right_hull) - 1) and \
                (yint(ulh_point, urh_point, midpoint, 0, sys.maxsize)) >= (yint(ulh_point, right_hull[right_hull.index(urh_point) + 1], midpoint, 0, sys.maxsize)) and \
                (right_hull[right_hull.index(urh_point) + 1][0] > urh_point[0]) and \
                (right_hull[right_hull.index(urh_point) + 1][1] < urh_point[1]):
            outlier = True
        elif (left_hull.index(ulh_point) != 0) and \
                (yint(ulh_point, urh_point, midpoint, 0, sys.maxsize)) >= (yint(left_hull[left_hull.index(ulh_point) - 1], urh_point, midpoint, 0, sys.maxsize)) and \
                (left_hull[left_hull.index(ulh_point) - 1][0] < ulh_point[0]) and \
                (left_hull[left_hull.index(ulh_point) - 1][1] < ulh_point[1]):
            outlier = True
        elif (right_hull_copy.index(lrh_point) != 0) and \
                (yint(llh_point, lrh_point, midpoint, 0, sys.maxsize)) <= (yint(llh_point, right_hull_copy[right_hull_copy.index(lrh_point) - 1], midpoint, 0, sys.maxsize)) and \
                (right_hull_copy[right_hull_copy.index(lrh_point) - 1][0] > lrh_point[0]) and \
                (right_hull_copy[right_hull_copy.index(lrh_point) - 1][1] > lrh_point[1]):
            outlier = True
        elif (left_hull_copy.index(llh_point) != len(left_hull_copy) - 1) and \
                (yint(llh_point, lrh_point, midpoint, 0, sys.maxsize)) <= (yint(left_hull_copy[left_hull_copy.index(llh_point) + 1], lrh_point, midpoint, 0, sys.maxsize)) and \
                (left_hull_copy[left_hull_copy.index(llh_point) + 1][0] < llh_point[0]) and \
                (left_hull_copy[left_hull_copy.index(llh_point) + 1][1]) > llh_point[1]:
            outlier = True

        if not outlier:
            binding_points = [ulh_point, urh_point, lrh_point, llh_point]
            points = list(set(points) ^ set(binding_points))
            removal = []

            x_min = min(binding_points, key=lambda point: point[0])
            x_max = max(binding_points, key=lambda point: point[0])
            y_min = min(binding_points, key=lambda point: point[1])
            y_max = max(binding_points, key=lambda point: point[1])

            for i in points:
                if (x_min[0] < i[0] < x_max[0]) and (y_min[1] < i[1] < y_max[1]):
                    removal.append(i)

            points = list(set(points) ^ set(removal) ^ set(binding_points))
            break
    return points

