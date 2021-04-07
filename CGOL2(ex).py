import pygame
 #this sets which are alive in the next generation
gamerunning = False

loadfile = ""
cellsize = 5 # has to be a factor of both width and height
width = 400 #maximum x value
height = 400 #maximum y value

def FindCellPos(index):
    if index<0 or index >= numcells:
        return [-1,-1]
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


if width%cellsize!=0 or height%cellsize!=0:
    print("Your value for cellsize is not a factor of width or height. Please input a different value and restart")
    quit()
cellnumx = int(width/cellsize)
cellnumy = int(height/cellsize)
numcells = cellnumx*cellnumy
celltransfer = [False]*int(numcells)
cells = [False]*int(numcells)
cellneighbors = []
        
def savefile(name):
    import pickle
    dumperdict = {"cells": cells,
                  "width": width,
                  "height": height,
                  "cellsize":cellsize}
    pickle.dump(dumperdict, open(name+".gol", "wb"))
    

#bytearray trutharray = ([])
def getbit(index):
    remainder = index%8
    arraypos = (index-remainder)/8
    bitmasks = []
    byte = bitcellarray[arraypos]
    bit = byte & bitmask
    bit = bit << remainder
    if bit == 0xFF:
        return True
    elif bit == 0x00:
        return False
def writebit(index):
    return
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
def executerules(index):
    global celltransfer, cells, cellneighbors
    neighbors = cellneighbors[index]
    aliveneighbors = []
    xpos, ypos = FindCellPos(index)
    for val in neighbors:
        if cells[val] == True:
            aliveneighbors.append(int(val))
    numalive = len(aliveneighbors)
    cellalive = cells[index]
    if (numalive == 3 or numalive == -1) and cellalive == False: #born
        celltransfer[index]=True
        drawcell(xpos, ypos, True)
    elif (numalive == 2 or numalive == 3) and cellalive==True: #survives
        celltransfer[index]=True
    elif cellalive == True:
        celltransfer[index]=False
        drawcell(xpos, ypos, False)
    


for q in range(numcells):
    cellneighbors.append(FindNeighbors(q))
print("ready")

toggledcells = []
saveiteration = 0
while True:
    if gamerunning:
        for i in range(numcells):
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
            