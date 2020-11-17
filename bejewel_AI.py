# python windows exe help:
#   https://medium.com/dreamcatcher-its-blog/making-an-stand-alone-executable-from-a-python-script-using-pyinstaller-d1df9170e263
#   http://bejeweled3.co/

# import to check if left or right mouse buttons were pressed
from win32 import win32api
from win32 import win32gui
# mouse control
import pyautogui
# image processing
from PIL import Image, ImageStat
import time
# drawing stuff
from tkinter import *
from queue import PriorityQueue


class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        self.counter -= 1
        return item
    
    def len(self):
        return self.counter
    
# code by Isai B. Bicourel
# https://www.codementor.io/isaib.cicourel/image-manipulation-in-python-du1089j1u
def convert_to_primary(rgb, code):
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
    if code == 'rgb':
        return r,g,b
    else:
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

# help found at https://www.rapidtables.com/web/color/RGB_Color.html
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

def gemDrop(m, cells):
    pass

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
            else:
                if xmatches > 2:
                    matches += xmatches
                    for k in range(xmatches):
                        coords.append([i,j-k-1])
#                    coords.append(['x',[i,j-xmatches],[i,j-1]])
#                    print('X matches = [%d][%d-%d]'% (i,j-xmatches,j-1))
                xmatches = 1
    for i in range(cells):
        if ymatches > 2:
            matches += ymatches
        ymatches = 1
        for j in range(1,cells):
            if m[j][i] != -1 and m[j-1][i] != -1 and m[j][i] == m[j-1][i]:
                ymatches = ymatches + 1
            else:
                if ymatches > 2:
                    matches += ymatches
                    for k in range(ymatches):
                        coords.append([j-k-1,i])
#                    coords.append(['y',[j-ymatches,i],[j-1,i]])
#                    print('Y matches = [%d-%d][%d]'% (j-ymatches,j-1,i))
                ymatches = 1
    return coords, matches

# references for mouseclicks found at:
#   https://pyautogui.readthedocs.io/en/latest/mouse.html
        
def main():
    # assign state to mouse button clicks
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    # get square size of matrix
####    cells = int(input("Input Matrix Square Size: "))
####    darkness = float(input("percent darkened .xx format: "))
    cells = 8
    darkness = .18
    
    # initialize matrices
    Matrix = [[0 for i in range(cells)]for j in range(cells)]
    rgbMatrix = [[0 for i in range(cells)]for j in range(cells)]
    visualMatrix = [[0 for i in range(cells)]for j in range(cells)]
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
        time.sleep(0.001)
    tk = Tk()
    canvas = Canvas(tk, width= w+2, height=h+2)
    tk.geometry("%dx%d+1100+150"% (w+2,h+2))
    tk.title("RGB Color Tile")
    canvas.pack()
    
    while True:
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
                # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
##                Matrix[j][i] = ImageStat.Stat(region.quantize(8,0,0,)).mean
##        for i in range(cells):
##            print(Matrix[i])
        # convert median rgb to primary color rgb or char representation
        for i in range(cells):
            for j in range(cells):
                rgbMatrix[j][i] = convert_to_primary(Matrix[j][i], 'rgb')
                visualMatrix[j][i] = convert_to_primary(Matrix[j][i], 'vis')
##        break
        # create visual canvas
        # TODO make a command line option later
        for i in range(cells):
            for j in range(cells):
                canvas.create_rectangle(i*cellWidth,
                                        j*cellHeight,
                                        i*cellWidth + cellWidth,
                                        j*cellHeight + cellHeight,
                                        fill='#%02x%02x%02x' % rgbMatrix[j][i])
        tk.update()
##        time.sleep(0.05)
##        break ## Debug breaker

        q = MyPriorityQueue()
        for i in range(cells):
            for j in range(1,cells):
                copy = [row[:] for row in visualMatrix]
                copy = swapCellsHoriz(i,j,j-1,copy)
                coords, matches = findMatches(copy,cells)
                if matches >0:
                    #q.put(coords,-matches)
                    q.put([[i,j],[i,j-1]], -matches)
                    print(coords)
                copy = [row[:] for row in visualMatrix]
                copy = swapCellsVert(i,j,j-1,copy)
                coords, matches = findMatches(copy,cells)
                if matches > 0:
                    #q.put(coords,-matches)
                    q.put([[j,i],[j-1,i]], -matches)
                    print(coords)

        for i in range(cells):
            print(visualMatrix[i])
        print("")
        
        #go through priority queue of moves and click
##        while q.len() > 0:
        for i in range(5):
##            print(q.get())
            if(q.len() == 0):
                time.sleep(.2)
                break
            clck1, clck2 = q.get()
##            print(clck1)
##            print(clck2)
            pyautogui.moveTo(x1+int(clck1[1]*cellWidth+cellWidth/2)
                             ,y1+int(clck1[0]*cellHeight+cellHeight/2))
            time.sleep(.001)
            pyautogui.click()
            pyautogui.moveTo(x1+int(clck2[1]*cellWidth+cellWidth/2)
                             ,y1+int(clck2[0]*cellHeight+cellHeight/2))
            time.sleep(.001)
            pyautogui.click()

        time.sleep(.001)
##        break ## Debug breaker


if __name__ == '__main__':
    main()
