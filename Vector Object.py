from math import atan, pi, sqrt


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
        newX = self.__x * scalar
        newY = self.__y * scalar
        return Vector(newX,newY)
        
    def add(self, other):
        newX = self.getX() + other.getX()
        newY = self.getY() + other.getY()
        return Vector(newX,newY)

    def getAngle(self, degrees=True):
        rad = atan(self.getY() / self.getX())
        if degrees:
            return rad * (180 / pi)
        else:
            return rad
          
    def getMagnitude(self):
        hypsq = self.getX()**2 + self.getY()**2
        return sqrt(hypsq)

    def dotProduct(self, other):
        return self.getX() * other.getX() + self.getY() * other.getY()

    def convexCombination(self, other, alpha):
        u = self.scalarMultiply(alpha)
        v = self.scalarMultiply(1 - alpha)
        return u.add(v)

#--------------------------------------------------------

    """ computes the convex hull of the points self and other via Graham Scan """
    def inConvexHull(self, other, point):
        points = [self, other, point]
        """ sorts the points in ascending y-coord, and then by 
        ascending x-coord with the same y-coord """
        points = sorted(points, key=lambda p: (p.getY(), p.getX()))
        """ creates an empty stack and pushes the first 
        two points onto it """
        hull = [points[0], points[1]]
        """ iterates over the remaining points and pushes each 
        onto it"""
        for p in points[2:]:
            hull.append(p)
            """ if current point causes stack to make a non-left turn, 
            pop penultimate point until a left-turn is made. Ensures that 
            the stack's points form the convex hull of the inputs """
            while len(hull) > 2 and (hull[-1].getX() - hull[-2].getX()) * (hull[-2].getY() - hull[-3].getY()) > (hull[-2].getX() - hull[-3].getX()) * (hull[-1].getY() - hull[-2].getY()):
                hull.pop(-2)

        """ for each edge, the input point is checked to
        ensure it's on the same side of the edge as the rest of
        the hull """ 
        for i in range(len(hull)):
            """ to do so, the cross product of the vector from
            the previous to the current, as well as from the current 
            to the next, point is calculated """
            v1 = hull[(i - 1) % len(hull)]
            v2 = hull[i]
            v3 = hull[(i + 1) % len(hull)]
            """ the input point lies within the hull if it's on the 
            same side of all the edges """
            if (v2.getY() > point.getY()) != (v3.getY() > point.getY()) and point.getX() < (v3.getX() - v2.getX()) * (point.getY() - v2.getY()) / (v3.getY() - v2.getY()) + v2.getX():
                return False
        return True

#------------------------------------------------------------
        
    def __str__(self):
        output = "({},{})".format(self.getX(), self.getY())
        return output

#-----------------------------------------------------------
      
v1 = Vector(2,2)
v2 = Vector(6,-2)
