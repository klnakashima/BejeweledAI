# python windows exe help:
#   https://medium.com/dreamcatcher-its-blog/making-an-stand-alone-executable-from-a-python-script-using-pyinstaller-d1df9170e263
#   http://bejeweled3.co/
#   Other resources:
#       https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
#       https://www.codementor.io/isaib.cicourel/image-manipulation-in-python-du1089j1u
#       https://www.rapidtables.com/web/color/RGB_Color.html
#       https://pyautogui.readthedocs.io/en/latest/mouse.html


# import to check if left or right mouse buttons were pressed
from win32 import win32api
from win32 import win32gui
# mouse control
import pyautogui
# image processing
from PIL import Image, ImageStat
import time

class Tree:
    def __init__(self, m):
        self.matrix = m
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def setList(self):
        temp = self.children
        temp = set(temp)
        self.children = list(temp)

class Node:
    def __init__(self,c1,c2,hval):
        self.c1 = c1
        self.c2 = c2
        self.hval = hval
    def __lt__(self, other):
        return self.hval > other.hval
    def __eq__(self, other):
        return self.c1 == other.c1 and self.c2 == other.c2
    def __hash__(self):
        return hash((self.c1[0], self.c1[1], self.c2[0], self.c2[1]))
    
def createTree(m,cells,t):
    for i in range(cells):
        for j in range(1,cells):
            copy1 = [row[:] for row in m]
            copy1 = swapCellsHoriz(i,j,j-1,copy1)
            coords, matches1 = findMatches(copy1,cells)
            if matches1 > 2:
                # add to tree
                copy1 = delCoords(coords, copy1)
                copy1 = gemDrop(copy1, cells)
                coords, matches2 = findMatches(copy1,cells)
                t.add_child(Node([i,j],[i,j-1], matches2 + matches1 ))
            copy2 = [row[:] for row in m]
            copy2 = swapCellsVert(i,j,j-1,copy2)
            coords, matches2 = findMatches(copy2,cells)
            if matches2 > 2:
                # add to tree
                copy1 = delCoords(coords, copy2)
                copy1 = gemDrop(copy2, cells)
                coords, matches2 = findMatches(copy2,cells)
                t.add_child(Node([j,i],[j-1,i], matches2 + matches1 ))
    return t
    
def convert_to_primary(rgb):
    r, g, b = rgb
    # Transform to primary
    if r > 128:
        r = 255
    else:
        r = 0
    if g > 170:
        g = 255
    elif g < 85:
        g = 0
    else:
        g = 127
    if b > 128:
        b = 255
    else:
        b = 0
    return colorCode(r, g ,b)

def swapCellsHoriz(i,j,k,m):
    n = m
    temp = n[i][j]
    n[i][j] = n[i][k]
    n[i][k] = temp
    return n

def swapCellsVert(i,j,k,m):
    n = m
    temp = n[j][i]
    n[j][i] = n[k][i]
    n[k][i] = temp
    return n

def colorCode(r, g, b):
    if (r == 255 and g == 0 and b == 0):
        return 'R' #red
    if (r == 255 and g == 127 and b == 0):
        return 'O' #orange
    if (r == 255 and g == 255 and b == 0):
        return 'Y' #yellow
    if (r == 0 and g == 255 and b == 0):
        return 'G' #green
    if (r == 0 and g == 127 and b == 255):
        return 'B' #blue
    if (r == 255 and g == 0 and b == 255):
        return 'P' #purple
    if (r == 255 and g == 255 and b == 255):
        return 'W' #white
    if (r == 0 and g == 0 and b == 0):
        return -1 #black

def delCoords(c,m):
    n = m
    for coords in c:
        i,j = coords
        n[i][j] = -1
    return n
    
def gemDrop(m, cells):
    n = m
    for k in range(cells):
        for i in range(cells):
            for j in range(cells):
                if n[j][i] == -1:
                    if j == 0:
                        n[j][i] = -1
                    else:
                        n[j][i] = n[j-1][i]
                        n[j-1][i] = -1
    return n

def findMatches(m,cells):
    coords = []
    matches = 0
    xmatches = 0
    ymatches = 0
    for i in range(cells):
        if xmatches > 2:
            matches += xmatches
            # add actual move
        xmatches = 1
        for j in range(1,cells):
            if m[i][j] != -1 and m[i][j-1] != -1 and m[i][j] == m[i][j-1]:
                xmatches = xmatches + 1
            elif m[i][j] == -1 or m[i][j-1] == -1:
                pass
            else:
                if xmatches > 2:
                    matches += xmatches
                    for k in range(xmatches):
                        coords.append([i,j-k-1])
                xmatches = 1
    for i in range(cells):
        if ymatches > 2:
            matches += ymatches
        ymatches = 1
        for j in range(1,cells):
            if m[j][i] != -1 and m[j-1][i] != -1 and m[j][i] == m[j-1][i]:
                ymatches = ymatches + 1
            elif m[j][i] == -1 or m[j-1][i] == -1:
                pass
            else:
                if ymatches > 2:
                    matches += ymatches
                    for k in range(ymatches):
                        coords.append([j-k-1,i])
                ymatches = 1
    return coords, matches

def main():
    # assign state to mouse button clicks
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    # initialize size of matrix
    cells = 8
    # adjust darkness to screenshot for color calibration
    darkness = .18
    
    # initialize matrices
    Matrix = [[0 for i in range(cells)]for j in range(cells)]
    # user #comment out after readme file created
####    print("left click at top left corner of jewel field, hold, and release at bottom right corner of jewel field")
    
    # loop for setting area of matrix     
    while True:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                x1, y1 = win32api.GetCursorPos()
            else:
                x2, y2 = win32api.GetCursorPos()
                w = x2 - x1
                h = y2 - y1
                cellWidth = w / cells
                cellHeight = h / cells
                break
        time.sleep(0.01)
    
    while True:
        visualMatrix = [[0 for i in range(cells)]for j in range(cells)]
        # screenshot board
        im = pyautogui.screenshot(region=(x1,y1,w,h))
        # darken image by 10%
        im = im.point(lambda x: x*(1-darkness))
        # get median rgb value of part of each cell
        for i in range(cells):
            for j in range(cells):
                box = (i*cellWidth + (cellWidth*(2/7)),
                       j*cellHeight + (cellHeight*(2/7)),
                       i*cellWidth + cellWidth- (cellWidth*(2/7)),
                       j*cellHeight + cellHeight- (cellHeight*(2/7)))
                region = im.crop(box)
                Matrix[j][i] = ImageStat.Stat(region).median
                
        # convert median rgb to primary color rgb or char representation
        for i in range(cells):
            for j in range(cells):
                visualMatrix[j][i] = convert_to_primary(Matrix[j][i])
##        break ## Debug breaker

        t = Tree(visualMatrix)
        t.children = []
        t = createTree(visualMatrix, cells, t)
        t.setList()
        t.children.sort()

##        break ## Debug breaker

        # click away
        counter = 0
        for child in t.children:
            if counter > 4:
                break
            clck1 = child.c1
            clck2 = child.c2
            pyautogui.moveTo(x1+int(clck1[1]*cellWidth+cellWidth/2)
                             ,y1+int(clck1[0]*cellHeight+cellHeight/2))
            time.sleep(.01)
            pyautogui.click()
            pyautogui.moveTo(x1+int(clck2[1]*cellWidth+cellWidth/2)
                             ,y1+int(clck2[0]*cellHeight+cellHeight/2))
            time.sleep(.01)
            pyautogui.click()
            counter += 1

##        time.sleep(.1)
##        break ## Debug breaker

if __name__ == '__main__':
    main()
