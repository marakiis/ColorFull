#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import math
import random

from PIL import Image

class Color:
    def norm(self):
        res = 0
        for i in range (0, 3):
            res = res + math.pow(self.colorTab[i],2)
        return math.sqrt(res)

    def __init__ (self, r, g, b):
        self.colorTab = [r, g, b]

    def __eq__ (self, other):
        for i in range (0, 3):
            if(self.colorTab[i] != other.colorTab[i]):
                return False
        return True

    def __hash__ (self):
        return hash(self.colorTab)

class Position:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def __eq__ (self, other):
        if (self.x == other.x) and (self.y == other.y):
            return True
        return False

    def __hash__ (self):
        return hash((self.x, self.y))

def colorsGenerator(maxComposante, nbColors):
    colorsGen = 0
    multiplier = 256/maxComposante
    colors = []
    for r in range (0, maxComposante):
        for g in range (0, maxComposante):
            for b in range (0, maxComposante):
                colors.append(Color(r*multiplier, g*multiplier, b*multiplier))
                colorsGen = colorsGen + 1
                if  colorsGen % 10000 == 0:
                    print "%r/%r colors generated" %(colorsGen, nbColors)
    return colors

def hueCalculator(c):
    return math.atan2(math.sqrt(3)*(c.colorTab[1]-c.colorTab[2]), 2*c.colorTab[0] - c.colorTab[1]-c.colorTab[2])

def hueSort(colors):
    nbColors = len(colors)
    sortedColors = 0
    res = []
    for color in colors:
        hue = hueCalculator(color)
        if(len(res) == 0):
            res.append(color)
        else:
            i = 0
            end = False
            bound = len(res) - 1
            while not end:
                if i > bound:
                    res.append(color)
                    end = True
                if hueCalculator(res[i]) > hue:
                    res.insert(i, color)
                    end = True
                i = i + 1
        sortedColors = sortedColors + 1
        if  sortedColors % 1000 == 0:
            print "%r/%r colors sorted" %(sortedColors, nbColors)
    return res

def fillImage (grid, x, y):
    image = Image.new("RGB", (x, y))
    for i in range (0, x):
        for j in range (0, y):
             image.putpixel((i, j),(grid[i][j].colorTab[0], grid[i][j].colorTab[1], grid[i][j].colorTab[2]))
    return image

def scalarProduct(c1, c2):
    res = 0
    for i in range (0, 3):
        res = res + c1.colorTab[i] * c2.colorTab[i]
    return res

def euclydeDist(c1, c2):
    res = 0
    for c in range (0, 3):
        res = math.pow(c1.colorTab[c] - c2.colorTab[c], 2)
    return res

def cosinus(c1, c2):
    div = (c1.norm()*c2.norm())
    if div == 0:
        div = 1
    return scalarProduct(c1, c2)/div

def barycenter(cases):
    blank = Color(-1,-1,-1)
    i = 0
    r = 0
    g = 0
    b = 0
    for case in cases:
        if not case.__eq__(blank):
            r = case.colorTab[0]
            g = case.colorTab[1]
            b = case.colorTab[2]
            i = i + 1
    return Color(r, g, b)

def updateFree(pos, grid, free, x, y):
    blank = Color(-1,-1,-1)
    color = grid[pos.x][pos.y]
    if pos.x + 1 < x:
        if grid[pos.x + 1][pos.y].__eq__(blank):
            upperRight = blank
            right = blank
            lowerRight = blank
            if pos.y + 1 < y:
                upperRight = grid[pos.x + 1][pos.y + 1]
            if pos.x + 2 < x:
                right = grid[pos.x + 2][pos.y]
            if pos.y - 1 >= 0:
                lowerRight = grid[pos.x + 1][pos.y - 1]
            free.update({Position((pos.x + 1), pos.y): barycenter([color, upperRight, right, lowerRight])})
    if pos.x - 1 >= 0:
        if grid[pos.x - 1][pos.y].__eq__(blank):
            upperLeft = blank
            left = blank
            lowerLeft = blank
            if pos.y + 1 < y:
                upperLeft = grid[pos.x - 1][pos.y + 1]
            if pos.x - 2 >= 0:
                left = grid[pos.x - 2][pos.y]
            if pos.y - 1 >= 0:
                lowerLeft = grid[pos.x - 1][pos.y - 1]
            free.update({Position((pos.x - 1), pos.y): barycenter([color, upperLeft, left, lowerLeft])})
    if pos.y + 1 < y:
        if grid[pos.x][pos.y + 1].__eq__(blank):
            upperLeft = blank
            up = blank
            upperRight = blank
            if pos.x - 1 >= 0:
                upperLeft = grid[pos.x - 1][pos.y + 1]
            if pos.y + 2 < y:
                up = grid[pos.x][pos.y + 2]
            if pos.x + 1 < x:
                upperRight = grid[pos.x + 1][pos.y + 1]
            free.update({Position(pos.x, (pos.y + 1)): barycenter([color, upperLeft, up, upperRight])})
    if pos.y - 1 >= 0:
        if grid[pos.x][pos.y - 1].__eq__(blank):
            lowerLeft = blank
            low = blank
            lowerRight = blank
            if pos.x - 1 >= 0:
                lowerLeft = grid[pos.x - 1][pos.y - 1]
            if pos.y - 2 >= 0:
                low = grid[pos.x][pos.y - 2]
            if pos.x + 1 < x:
                lowerRight = grid[pos.x + 1][pos.y - 1]
            free.update({Position(pos.x, (pos.y - 1)): barycenter([color, lowerLeft, low, lowerRight])})

def addPixelMinDist(image, grid, free, color, x, y):
    min = -1
    for position in free:
        dist = cosinus(free[position], color)
        if (dist == min) :
            selected.append(position)
        if (dist < min) or (min == -1):
            min = dist
            selected = [position]
    choosen = selected[int(random.uniform(0, len(selected)))]
    grid[choosen.x][choosen.y] = color
    del free[choosen]
    updateFree(choosen, grid, free, x, y)

def addPixelMaxCos(image, grid, free, color, x, y):
    max = 2
    for position in free:
        dist = cosinus(free[position], color)
        if (dist == max) :
            selected.append(position)
        if (dist > max) or (max == 2):
            max = dist
            selected = [position]
    choosen = selected[int(random.uniform(0, len(selected)))]
    grid[choosen.x][choosen.y] = color
    del free[choosen]
    updateFree(choosen, grid, free, x, y)

def fillPixelRandom (grid, colors, x, y):
    tabSize = len(colors) - 1
    for i in range(0, x):
        for j in range(0, y):
            chosen = int(random.uniform(0, tabSize))
            grid[i][j] = colors.pop(chosen)
            tabSize = tabSize - 1
            if tabSize < 0:
                return grid
    return grid

def fillPixelRandomMinDist(grid, colors, x, y):
    tabSize = len(colors) - 1
    free = {Position(0, 0): (Color(0, 0, 0))}
    image = Image.new("RGB", (x, y))
    while tabSize > 0:
        chosen = int(random.uniform(0, tabSize))
        addPixelMinDist(image, grid, free, colors.pop(chosen), x, y)
        tabSize = tabSize - 1
        if(tabSize%1000 == 0):
            print "%r, %r" %(len(free), tabSize,)
    return grid

def fillPixelRandomMaxCos(grid, colors, x, y):
    tabSize = len(colors) - 1
    free = {Position(0, 0): (Color(0, 0, 0))}
    image = Image.new("RGB", (x, y))
    while tabSize > 0:
        chosen = int(random.uniform(0, tabSize))
        addPixelMaxCos(image, grid, free, colors.pop(chosen), x, y)
        tabSize = tabSize - 1
        if(tabSize%1000 == 0):
            print "%r, %r" %(len(free), tabSize,)
    return grid

def fillPixelMinDist(grid, colors, x, y):
    tabSize = len(colors)
    free = {Position(int(x/2), int(y/2)): (Color(0, 0, 0))}
    image = Image.new("RGB", (x, y))
    while tabSize > 0:
        addPixelMinDist(image, grid, free, colors.pop(0), x, y)
        tabSize = tabSize - 1
        if(tabSize%1000 == 0):
            print "%r, %r" %(len(free), tabSize,)
    return grid

def fillPixelMaxCos(grid, colors, x, y):
    tabSize = len(colors)
    free = {Position(0, 0): (Color(0, 0, 0))}
    image = Image.new("RGB", (x, y))
    while tabSize > 0:
        addPixelMaxCos(image, grid, free, colors.pop(0), x, y)
        tabSize = tabSize - 1
        if(tabSize%1000 == 0):
            print "%r, %r" %(len(free), tabSize,)
    return grid

print "Start Pixel Bo"
bitPerColor = 15
totalColors = int(math.pow(2, bitPerColor))
maxComposante = int(math.pow(2, bitPerColor/3))

# Generation of the colors
print "Generation of the %r colors" %(totalColors)
colors = colorsGenerator(maxComposante, totalColors)
print "%r/%r generated colors" %(len(colors), totalColors,)

# Creation of the color tab
x = int(4*math.sqrt(totalColors)/3+1)
y = int(3*math.sqrt(totalColors)/4+1)
print "Tab size : %r (%r, %r)" %(x*y, x, y,)

# Creation of the color grid
print "Generation of the table"
grid = []
for i in range(0, x):
    collumn = []
    for j in range(0, y):
        collumn.append(Color(-1,-1,-1))
    grid.append(collumn)

# HUE sorting
colors = hueSort(colors)

print "Start filling the table"
grid = fillPixelMaxCos(grid, colors, x, y)
print "Table filled"
print "Start Creation of the image"
image = fillImage(grid, x, y)
image.save("result.png", "PNG")
print "Image created and saved"
print "End Pixel Bo"
