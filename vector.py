import math
from math import acos, degrees, sqrt, atan2
import matplotlib.pyplot as plt


class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
  
    def scalar_multiply(self, scalar):
        new_x = self.x * scalar
        new_y = self.y * scalar
        return Vector(new_x, new_y)
        
    def add(self, other):
        new_x = self.get_x() + other.get_x()
        new_y = self.get_y() + other.get_y()
        return Vector(new_x, new_y)

    """ describes a weighted sum of points w/ the condition that weights alpha and gamma must sum to 1. """
    def convex_combination(self, other, alpha, gamma):
        if alpha + gamma != 1:
            raise ValueError("Coefficients must sum to 1.")
        if alpha < 0 or gamma < 0:
            raise ValueError("Neither coefficient can be negative.")
        new_x = alpha * self.get_x() + gamma * other.get_x()
        new_y = alpha * self.get_y() + gamma * other.get_y()
        return Vector(new_x, new_y)

    def show_angle(self, other, in_degrees = True):
        dot_product = self.dot_product(other)
        magnitude_product = self.show_magnitude() * other.show_magnitude()
        """ math.acos() returns the arc (inverse) cosine of a value between -1 and 1. """
        angle_radians = math.acos(dot_product / magnitude_product)
        if in_degrees:
            """ math.degrees() converts from radians, an angular measure defined such that an angle of one radian subtended from the 
            center of a circle produces an arc of length 1."""
            return math.degrees(angle_radians)
        else:
            return angle_radians

    def normalise(self):
        magnitude = self.show_magnitude()
        if magnitude == 0:
            return Vector(0, 0)
        else:
            return Vector(self.get_x() / magnitude, self.get_y() / magnitude)
          
    def show_magnitude(self):
        return math.sqrt(self.get_x() ** 2 + self.get_y() ** 2)

    """ describes the sum of the products of the corresponding components in each vector. """
    def dot_product(self, other):
        return self.get_x() * other.get_y() + self.get_y() * other.get_y()

        """ computes the convex hull (the smallest convex set that contains all points of a given set of (x, y) coordinates S) 
        via Graham Scan. Convex describes a shape in which the counterclockwise traversal of its vertices may never acquire a 
        clockwise rotation. """
    def __construct_convex_hull(self, points):
        self.points = points
        """ finhd the point w/ te lowest y-coord; consider the smaller x-coordinate if points share a y-coord. """
        lowest = min(self.points, key = lambda p: (p[1], p[0]))

        """ sort the remaining 'n - 1' points by counterclockwise polar angle (counterclockwise angle from the x-axis at which 
        a point in the xy-plane lies) around 'lowest'. """
        def __polar_angle(p):
            x, y = p[0] - lowest[0], p[1] - lowest[1]
            """ math.atan2() returns the arc tangent (in radians) of y / x. Unlike math.atan(y / x), the signs of both coordinates 
            are considered. """
            return math.atan2(y, x)

        sorted_points = sorted([p for p in self.points if p != lowest], key = __polar_angle)
        """ push first three points. """
        stack = [lowest, sorted_points[0], sorted_points[1]]

        """ for each point p in the sorted list (except for the first two which have already been pushed), check whether 
        p is to the left or right of the line formed by the last two points on the stack. If it's to the left of the line, 
        push it, and if it's to the right, pop the last point off the stack and repeat the test w/ the new last point and p. """
        for p in sorted_points[2:]:
            while len(stack) > 1 and (p[0] - stack[-2][0]) * (stack[-1][1] - stack[-2][1]) >= (p[1] - stack[-2][1]) * (stack[-1][0] - stack[-2][0]):
                stack.pop()
            stack.append(p)
   
        return stack[::-1]

    def display_convex_hull(self, points):
        hull_points = self.__construct_convex_hull(points)
        x = [p[0] for p in hull_points]
        y = [p[1] for p in hull_points]
        """ plt.plot plots lists across their respective axes; ro- represents a plot using red circle markers. """
        plt.plot(x, y, 'ro-')
        """ '.show' displays the plot. """
        plt.show()

    def show_bector(self):
        return f"({round(self.get_x(), 1)}, {round(self.get_y(), 1)})"
