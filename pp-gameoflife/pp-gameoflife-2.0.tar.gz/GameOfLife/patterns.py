# -*- coding: utf-8 -*-
import numpy as np

def cross(h,w):
    """
    Creates cross-shaped pattern. Grid of size hxw.
    
    Parameters
    ----------
    h : integer
    w : integer
    
    Returns
    -------
    cross : hxw array
    
    """
    cross = np.zeros([h,w])
    cross[int(h/2),:] = 1    
    cross[:,int(w/2)] = 1
    if np.mod(h,2) != 1:
        cross[int(h/2)-1,:] = 1   
    if np.mod(w,2) != 1:
        cross[:,int(w/2)-1] = 1
    return cross

def cube(h,w):
    """
    Creates cube-shaped pattern. Grid of size hxw.
    
    Parameters
    ----------
    h : integer
    w : integer
    
    Returns
    -------
    cube : hxw array
    
    """
    cube = np.zeros([h,w])
    cube[int(3*h/8):int(5*h/8),int(3*w/8):int(5*w/8)] = 1
    #cube[:,int(3*w/8):int(5*w/8)] = 1
    return cube

def checker(h,w):
    """
    Creates checker-board pattern. Grid of size hxw.
    
    Parameters
    ----------
    h : integer
    w : integer
    
    Returns
    -------
    checker: hxw array
    
    """
    c0 = [[1,0],[0,1]]
    checker = np.tile(c0,(int(h/2),int(w/2)))        
    return checker

def random(h,w):
    """
    Creates random pattern. Grid of size hxw.
    
    Parameters
    ----------
    h : integer
    w : integer
    
    Returns
    -------
    random : hxw array
    
    """
    random = np.random.randint(0,2,h*w).reshape([h,w])
    return random

def stripes(h,w,mode = 0):
    """
    Creates stripes pattern. Grid of size hxw.
    
    Parameters
    ----------
    h : int
    w : int
    
    mode : int, optional
           0 ... 2 stripes from top left to lower right
           1 ... 2 stripes from bottom left to upper right
           2 ... stripes from mode=0 and mode=1 combined
    
    Returns
    -------
    stripes: hxw array
    
    """
    s = np.ones(h-2)
    stripes = np.zeros([h,w])
    stripes += np.diag(s,2) + np.diag(s,-2)
    if mode == 1:
        stripes = np.flip(stripes,0)
    if mode == 2:
        stripes = stripes + np.flip(stripes,0)
    return stripes

def glider(h,w):
    """
    Creates a glider on the top left. Grid of size hxw.
    
    Parameters
    ----------
    h : integer
    w : integer
    
    Returns
    -------
    glider : hxw array
    
    """
    glider = np.array([[0,0,1],[1,0,1],[0,1,1]])
    g = np.zeros([h,w])
    g[0:3,0:3] = glider
    return g