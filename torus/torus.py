import numpy as np
import math
import matplotlib.pyplot as plt


class Point:
    """A point in 2d coordinates."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
        
    @staticmethod
    def torus_coodinates(x, y, torus_length, torus_width):
        """Return the coordinates in torus."""
        return x % torus_length, y % torus_width
         
    @classmethod
    def in_torus(cls, x, y, torus):
        """Constructor with given torus"""
        return cls(*cls.torus_coodinates(x, y, torus.length, torus.width))
    
    def place_in_torus(self, torus):
        """Return the point placed in torus coordinates"""
        return  Point(*self.torus_coodinates(self.x, self.y, torus.length, torus.width))
    
    def left(self, torus):
        return Point(self.x - torus.length, self.y)
    
    def right(self, torus):
        return Point(self.x + torus.length, self.y)
    
    def up(self, torus):
        return Point(self.x, self.y + torus.width)
    
    def down(self, torus):
        return Point(self.x, self.y - torus.width)
    
    def plot(self, color='b', marker='.'):
        plt.scatter(self.x, self.y, c=color, marker=marker)

        
class Torus:
    """A rectangle torus."""
    
    def __init__(self, length, width):
        self.length = length
        self.width = width
        
              
def distance_torus(point1, point2, torus):
    """Return the distance between two points on a torus."""
    other_points = [point2, point2.left(torus), point2.right(torus), point2.up(torus), point2.down(torus)]
    flags = ["in", "left", "right", "up", "down"]
    distances = [euclidian_dist(point1, point) for point in other_points]
    return min(distances), flags[np.argmin(distances)]
    

def euclidian_dist(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def plot_segment(p1, p2, color='r'):
    plt.plot([p1.x, p2.x], [p1.y, p2.y], color=color)
    
def draw_torus_line(p1, p2, torus, how='in'):
    """Draw line between two points in torus wrap mode."
    
    Parameters
    ----------
    p1, p2 : Point
        the two extremities (order matters)
    how : {'in', left', 'right', 'up', 'down'}
        indicates on which torus edge the line go through; 'in' means without crossing edges.
        
    Return
    ------
    None
    
    """
    if how == 'in':
        plot_segment(p1, p2)
    elif how == 'left':
        anchor_left = left_anchor(p1, p2, torus)
        anchor_right = Point(torus.length, anchor_left.y)
        plot_segment(p1, anchor_left)
        plot_segment(anchor_right, p2)
    elif how == 'right':
        anchor_right = right_anchor(p1, p2, torus)
        anchor_left = Point(0, anchor_right.y)
        plot_segment(p1, anchor_right)
        plot_segment(anchor_left, p2)
    elif how == 'up':
        anchor_up = up_anchor(p1, p2, torus)
        anchor_down = Point(anchor_up.x, 0)
        plot_segment(p1, anchor_up)
        plot_segment(anchor_down, p2)
    elif how == 'down':
        anchor_down = down_anchor(p1, p2, torus)
        anchor_up = Point(anchor_down.x, torus.width)
        plot_segment(p1, anchor_down)
        plot_segment(anchor_up, p2)
        
def draw_shortest_path(p1, p2, torus, show_points=True):
    """Draw shortest line between them on a torus."""
    if show_points:
        p1.plot()
        p2.plot()
    dist, how = distance_torus(p1, p2, torus)
    draw_torus_line(p1, p2, torus, how=how)
        
def left_anchor(p1, p2, torus):
    p2_l = p2.left(torus)
    _, b = line_eq(p1, p2_l)
    return Point(0, b)
    
def right_anchor(p1, p2, torus):
    p2_r = p2.right(torus)
    a, b = line_eq(p1, p2_r)
    x = torus.length
    y = a * x + b
    return Point(x, y)

def up_anchor(p1, p2, torus):
    if p1.x == p2.x:
        return Point(p1.x, torus.width)
    else:
        p2_u = p2.up(torus)
        a, b = line_eq(p1, p2_u)
        y = torus.width
        x = (y - b) / a
        return Point(x, y)

def down_anchor(p1, p2, torus):
    if p1.x == p2.x:
        return Point(p1.x, 0)
    else:
        p2_d = p2.down(torus)
        a, b = line_eq(p1, p2_d)
        return Point(-b/a, 0)
    
def line_eq(p1, p2):
    """Return slope and intercept of a line defined by two points.
    
    Raise ValueError if p1.x == p2.x (vertical line)
    """
    if p1.x == p2.x:
        raise ValueError('p1.x == p2.x : line is vertical (infinite slope)')
    slope = (p2.y - p1.y) / (p2.x - p1.x)
    intercept = p1.y - slope * p1.x
    return slope, intercept