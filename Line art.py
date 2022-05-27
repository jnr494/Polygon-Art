# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 21:17:27 2022

@author: mrgna
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import colorsys

#Polygon functions functions
def initArea(length, height):
    return [[(0,0),(0,height),(length,height),(length,0)]]

def randomPolygon(polygons):
    n = len(polygons)
    return np.random.randint(n,size = 1)[0]

def getAreaofPolygon(polygon):
    areaterms = [x1*y2-x2*y1 for (x1,x2),(y1,y2) in zip(polygon,polygon[1:] + polygon[:1])]
    area = np.abs(np.sum(areaterms)/2)
    return area

def LargestPolygon(polygons):
    areas = [getAreaofPolygon(polygon) for polygon in polygons]
    return np.argmax(areas)

def SmallestPolygon(polygons):
    areas = [getAreaofPolygon(polygon) for polygon in polygons]
    return np.argmin(areas)
    
#Edge functions

def randomEdges(polygon):
    n = len(polygon)
    chosenEdges = np.sort(np.random.choice(range(n),size = 2, replace = False))
    return chosenEdges

def RandomPointOnEdge(polygon, chosenEdge):
    point1 = np.array(polygon[chosenEdge])
    point2 = np.array(polygon[chosenEdge+1 if chosenEdge < (len(polygon)-1) else 0])
    
    PointsDiff = point2 - point1
    lengthOfEdge = np.sqrt(np.sum((PointsDiff)**2))
    
    angle = np.arctan2(PointsDiff[1],PointsDiff[0])
    
    placeOnEdge = np.random.uniform(size = 1,low=0.3,high=0.7)[0]
    newLength = placeOnEdge * lengthOfEdge

    newPoint = (point1[0] + newLength*np.cos(angle),point1[1] + newLength*np.sin(angle))
    
    return newPoint

#Main Functions

def newPolygons(polygons,dividemethod = 'largest'):
    #choose polygon
    if dividemethod == 'largest':
        chosenPolygon = LargestPolygon(polygons)
    elif dividemethod == 'smallest':
        chosenPolygon = SmallestPolygon(polygons)
    elif dividemethod == 'random':
        chosenPolygon = randomPolygon(polygons)
    else:
        chosenPolygon = randomPolygon(polygons)
    
    #choose edge
    chosenEdges = randomEdges(polygons[chosenPolygon])
    
    
    newPoints = [RandomPointOnEdge(polygons[chosenPolygon],i) for i in chosenEdges]
    
    newPolygons = []
    for i, polygon in enumerate(polygons):
        if i == chosenPolygon:
            #newArea1
            newPolygon1 = newPoints[0:1] + polygon[(chosenEdges[0]+1):(chosenEdges[1]+1)] + newPoints[1:]
            newPolygons.append(newPolygon1)
            
            #newArea2
            newPolygon2 = polygon[0:(chosenEdges[0]+1)] + newPoints + polygon[(chosenEdges[1]+1):]
            newPolygons.append(newPolygon2)
        else:
            newPolygons.append(polygon)
    
    return newPolygons

def generatePolygons(nPolygons,length = 1, dividemethod='largest'):
    polygons = initArea(length,1)
    for _ in range(nPolygons-1):
        
        polygons = newPolygons(polygons,dividemethod=dividemethod)
    return polygons

#Plot functions
def getHSLColor():
    h = np.random.uniform()/1.0 + 0.0
    s = np.random.uniform()*0.2 + 0.8
    l = np.random.uniform()*0.2 + 0.4
    return [i for i in colorsys.hls_to_rgb(h,l,s)]

def plotPolygonsAx(polygons, ax, edgecolor='w', linewidth=10, colorgenerator = lambda: np.random.uniform(size=3)):
    for polygon in polygons:
        color = colorgenerator()
        xpolygon = Polygon(np.array(polygon),
                           alpha=0.9,
                           facecolor = color,
                           edgecolor=edgecolor,
                           linewidth=linewidth)
        ax.add_patch(xpolygon)

def plotPolygons(polygons,length=1):
    figsize = 10
    height = 1
    fig, ax = plt.subplots(figsize=(length*figsize,height*figsize))
    plotPolygonsAx(polygons,ax,linewidth=figsize, colorgenerator=getHSLColor)
    plt.xlim(0, length)
    plt.ylim(0, height)
    plt.axis("off")
    fig.set_dpi(100)
    plt.xlim(0, length)
    plt.ylim(0, height)
    plt.show()

if __name__ == '__main__':
    length = 16/9 #as ratio from height
    dividemethod = 'largest' #choose from 'largest', 'smallest' and 'random'
    nPolygons = 10
    
    #Generate seeds
    np.random.seed(None)
    seedPolygon = np.random.randint(0,2**20,1)[0]
    seedColor = np.random.randint(0,2**20,1)[0]
    
    print("Polygon seed:", seedPolygon)
    print("Color seed:", seedColor)
    
    #Generate polygons
    np.random.seed(seedPolygon)
    polygons = generatePolygons(nPolygons,length,dividemethod)
    
    #Plot polygons
    np.random.seed(seedColor)
    plotPolygons(polygons,length)
    
    
    

    
    
