import pygame
 #this sets which are alive in the next generation
gamerunning = False

loadfile = ""
cellsize = 2
width = 400 #maximum x value
height = 400 #maximum y value


     
cellnumx = width/cellsize
cellnumy = height/cellsize
numcells = cellnumx*cellnumy
cells = [False]*int(numcells)

def FindCellPos(index):
    if index<0 or index >= numcells:
        return [int(-1),int(-1)]
    x = (index%cellnumx)
    y = ((index-x)/cellnumx)
    return [int(x*cellsize), int(y*cellsize)]

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Conway's Game of Life")
if loadfile != "":
    import pickle
    loaddict = pickle.load(open(loadfile + ".gol", "rb"))
    cellsize = loaddict["cellsize"]
    width = loaddict["width"]
    height = loaddict['height']
    cells = loaddict["cells"]
    for i in range(len(cells)-1):
        posx, posy = FindCellPos(i)
        rect = pygame.Rect(posx,posy,cellsize,cellsize)
        if cells[i]:
            pygame.draw.rect(screen, (255,255,255), rect)
        else:
            pygame.draw.rect(screen, (0,0,0), rect)
        pygame.display.update()
cellnumx = width/cellsize
cellnumy = height/cellsize
numcells = cellnumx*cellnumy
celltransfer = [False]*int(numcells)
        
def savefile(name):
    import pickle
    dumperdict = {"cells": cells,
                  "width": width,
                  "height": height,
                  "cellsize":cellsize}
    pickle.dump(dumperdict, open(name+".gol", "wb"))
#bytearray trutharray = ([])
def drawcell(x, y, alive):
    global cellsize
    rect = pygame.Rect(x,y,cellsize,cellsize)
    if alive:
        pygame.draw.rect(screen, (255,255,255), rect)
    else:
        pygame.draw.rect(screen, (0,0,0), rect)
    pygame.display.update()
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
    numalive = len(aliveneighbors)
    cellalive = cells[index]
    if (numalive == 3 or numalive == -1) and cellalive == False: #born
        celltransfer[index]=True
        drawcell(xpos, ypos, True)
    elif (numalive == 3 or numalive == 2) and cellalive==True: #survives
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "space":
                        gamerunning = not gamerunning
        cells = celltransfer
        celltransfer = [False]*int(numcells)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "space":
            gamerunning = not gamerunning
        if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "s":
            savefile("my simulation " + str(saveiteration))
            saveiteration+=1
        if not pygame.mouse.get_pressed()[0]:
            toggledcells = []
        if pygame.mouse.get_pressed()[0]:
            mousex, mousey = pygame.mouse.get_pos()
            specificcell = FindCellIndex(mousex, mousey)
            
            if (specificcell not in toggledcells) and specificcell!=-1:
                if cells[specificcell] == True:
                    cells[specificcell] = False
                else:
                    cells[specificcell] = True
                drawcell(mousex - (mousex % cellsize), mousey - (mousey % cellsize), cells[specificcell])
                toggledcells.append(specificcell)
            