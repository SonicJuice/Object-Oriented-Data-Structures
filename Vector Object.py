from math import acos, degrees, sqrt, atan2
import matplotlib.pyplot as plt


class Vector(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y
  
    def scalarMultiply(self, scalar):
        new_x = self.__x * scalar
        new_y = self.__y * scalar
        return Vector(new_x, new_y)
        
    def add(self, other):
        new_x = self.getX() + other.getX()
        new_y = self.getY() + other.getY()
        return Vector(new_x, new_y)

    """ describes a weighted sum of points w/ the condition that weights 'alpha' and 'gamma' must sum to 1. """
    def convexCombination(self, other, alpha, gamma):
        if alpha + gamma != 1:
            raise ValueError("Coefficients must sum to 1.")
        if alpha < 0 or gamma < 0:
            raise ValueError("Neither coefficient can be negative.")
        new_x = alpha * self.getX() + gamma * other.getX()
        new_y = alpha * self.getY() + gamma * other.getY()
        return Vector(new_x, new_y)

    def showAngle(self, other, in_degrees = True):
        dot_product = self.dotProduct(other)
        magnitude_product = self.showMagnitude() * other.showMagnitude()
        """ 'acos()' returns the arc (inverse) cosine of a value between -1 and 1. """
        angle_radians = acos(dot_product / magnitude_product)
        if in_degrees:
            """ 'degrees' converts from radians, an angular measure defined such that an angle of one radian subtended from the center of a circle produces an arc of length 1."""
            return degrees(angle_radians)
        else:
            return angle_radians

    def normalise(self):
        magnitude = self.showMagnitude()
        if magnitude == 0:
            return Vector(0, 0)
        else:
            return Vector(self.getX() / magnitude, self.getY() / magnitude)
          
    def showMagnitude(self):
        return sqrt(self.getX() ** 2 + self.getY() ** 2)

    """ describes the sum of the products of the corresponding components in each vector. """
    def dotProduct(self, other):
        return self.getX() * other.getX() + self.getY() * other.getY()

        """ computes the convex hull (the smallest convex set that contains all points of a given set of '(x, y)' coordinates 'S') via Graham Scan. Convex describes a shape in which the counterclockwise traversal of its vertices may never acquire a clockwise rotation. """
    def constructConvexHull(self, points):
        self.__points = points
        """ find the point w/ the lowest y-coord; consider the smaller x-coordinate if points share a y-coord. """
        lowest = min(self.__points, key = lambda p: (p[1], p[0]))

        """ sort the remaining 'n - 1' points by counterclockwise polar angle (counterclockwise angle from the x-axis at which a point in the xy-plane lies) around 'lowest'. """
        def polarAngle(p):
            x, y = p[0] - lowest[0], p[1] - lowest[1]
            """ 'atan2' returns the arc tangent (in radians) of 'y/x'. Unlike 'atan(y / x)', the signs of both coordinates are considered. """
            return atan2(y, x)

        sorted_points = sorted([p for p in self.__points if p != lowest], key = polarAngle)
        """ push first three points. """
        stack = [lowest, sorted_points[0], sorted_points[1]]

        """ for each point 'p' in the sorted list (except for the first two which have already been pushed), check whether 'p' is to the left or right of the line formed by the last two points on the stack. If it's to the left of the line, push it, and if it's to the right, pop the last point off the stack and repeat the test w/ the new last point and 'p'. """
        for p in sorted_points[2:]:
            while len(stack) > 1 and (p[0] - stack[-2][0]) * (stack[-1][1] - stack[-2][1]) >= (p[1] - stack[-2][1]) * (stack[-1][0] - stack[-2][0]):
                stack.pop()
            stack.append(p)
   
        return stack[::-1]

    def displayConvexHull(self, points):
        hull_points = self.constructConvexHull(points)
        x = [p[0] for p in hull_points]
        y = [p[1] for p in hull_points]
        """ '.plot' plots lists across their respective axes; 'ro-' represents a plot using red circle markers. """
        plt.plot(x, y, 'ro-')
        """ '.show' displays the plot. """
        plt.show()

    def showVector(self):
        return f"({round(self.getX(), 1)}, {round(self.getY(), 1)})"
