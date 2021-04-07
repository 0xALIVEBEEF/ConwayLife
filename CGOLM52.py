
 #this sets which are alive in the next generation
gamerunning = False




cellsize = 10
width = 320 #maximum x value
height = 240 #maximum y value
cellnumx = width/cellsize
cellnumy = height/cellsize
numcells = cellnumx*cellnumy
cells = [False]*int(numcells)
cellnumx = width/cellsize
cellnumy = height/cellsize
numcells = cellnumx*cellnumy
celltransfer = [False]*int(numcells)

from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5stack import touch

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

#bytearray trutharray = ([])
def drawcell(x, y, alive):
    global cellsize
    if alive:
        lcd.rect(x, y, cellsize, cellsize, fillcolor=0xffffff)
    else:
        lcd.rect(x, y, cellsize, cellsize, fillcolor=0x000000)
def FindCellPos(index):
    if index<0 or index >= numcells:
        return [int(-1),int(-1)]
    x = (index%cellnumx)*cellsize
    y = ((index-(index%cellnumx))/cellnumx)*cellsize
    return [int(x), int(y)]
def WriteBit(pos, value):
    bitpos = (pos%8)
    bytepos = (pos-bitpos)/8
    trutharray[bytepos] = trutharray[bytepos] & (0x01>>bitpos)
    
def ReadBit(pos, value):
    bitpos = (pos%8)
    bytepos = (pos-bitpos)/8
    trutharray[bytepos] = trutharray[bytepos] & (0x01>>bitpos)
    
def FindCellIndex(x,y):
    global width, height, cellsize
    if x >= width or y >= height or x < 0 or y < 0:
        return -1
    cellposx = (x - x % cellsize) / cellsize
    cellposy = (y - y % cellsize) / cellsize
    return int(cellposx + cellposy * cellnumx)
def FindNeighbors1(index): #This one horizontally teleports
    global cellnumx
    neighbors = []
    initialset = [(index - cellnumx) - 1, (index - cellnumx), (index - cellnumx) + 1,
                  index-1, index+1,
                  (index + cellnumx) - 1, (index + cellnumx), (index + cellnumx) + 1] #replace with x, y values, then eliminate values out of range, then find index values
    for val in initialset:
        if val >= 0 and val < numcells:
            neighbors.append(val)
    return neighbors
def FindNeighbors(index):
    global cellnumx
    xpos, ypos = FindCellPos(index)
    neighbors = []
    neighborset = [[-1, -1], [0, -1], [1, -1],
                  [-1, 0], [1, 0],
                  [-1, 1], [0, 1], [1, 1]]
    for offset in neighborset:
        offsettedvalue = [(offset[0]*cellsize)+xpos, (offset[1]*cellsize)+ypos]
        if offsettedvalue[0] < width and offsettedvalue[0] >= 0 and offsettedvalue[1] < height and offsettedvalue[1] >= 0 and offsettedvalue[0] % cellsize == 0 and offsettedvalue[1] % cellsize == 0:
            neighbors.append(FindCellIndex(offsettedvalue[0], offsettedvalue[1]))
    return neighbors
def executerules(index):
    global celltransfer, cells
    neighbors = FindNeighbors(index)
    aliveneighbors = []
    xpos, ypos = FindCellPos(index)
    for val in neighbors:
        if cells[int(val)] == True:
            aliveneighbors.append(int(val))
    cellalive = cells[index]
    if len(aliveneighbors) == 3 and cellalive == False:
        celltransfer[index]=True
        drawcell(xpos, ypos, True)
    elif (len(aliveneighbors) == 3 or len(aliveneighbors) == 2) and cellalive==True:
        celltransfer[index]=True
    elif cellalive == True:
        celltransfer[index]=False
        drawcell(xpos, ypos, False)
    



toggledcells = []
saveiteration = 0
while True:
    if gamerunning:
        for i in range(0, len(cells)-1):
            executerules(i)
            if btnC.wasPressed():
                gamerunning = not gamerunning
        cells = celltransfer
        celltransfer = [False]*int(numcells)
    if btnC.wasPressed():
        gamerunning = not gamerunning
    if not touch.status():
        toggledcells = []
    if touch.status():
        touchx, touchy = pygame.mouse.get_pos()
        specificcell = FindCellIndex(touchx, touchy)
        if (specificcell not in toggledcells) and specificcell!=-1:
            cells[specificcell] = not cells[specificcell]
            drawcell(touchx - (touchx % cellsize), touchy - (touchy % cellsize), cells[specificcell])
            toggledcells.append(specificcell)
            