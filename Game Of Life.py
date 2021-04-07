import pygame
import math
import time
gridwidth = 150
gridheight = 150
cellnum=gridheight*gridwidth
cellsize= 5
screenheight = gridheight * cellsize
screenwidth = gridwidth * cellsize
LOADFILE = "glidergun.gol"
def getneighbors(compcell):
    neighbors = []
    for row in grid:
        for cell in row:
            if (((abs(cell.x-compcell.x)+abs(cell.y-compcell.y))==cellsize) or ((abs(cell.x-compcell.x)==cellsize) and (abs(cell.y-compcell.y)==cellsize))):
                neighbors.append(cell)
    return neighbors
def executerules(cell):
    numalive = 0
    for neighbor in cell.neighbors:
        if neighbor.alive:
            numalive = numalive+1
    if (numalive == 1 or numalive == 3 or numalive == 5 or numalive == 7) and not cell.alive: #born
        cell.exempt = True
    if (numalive == 1 or numalive == 3 or numalive == 5 or numalive == 7) and cell.alive: #survive
        cell.exempt = True
class cell:
    def __init__(self, x, y, alive, size):
        self.x = x
        self.y= y
        self.alive = alive
        self.size = size
        self.rect = pygame.Rect(self.x,self.y,self.size,self.size)
        self.toggled = False
        self.neighbors = []
        self.exempt=False
        if self.alive:
            pygame.draw.rect(screen, (0,0,0), self.rect)
        else:
            pygame.draw.rect(screen, (255,255,255), self.rect)
        pygame.display.update()
    def redraw(self):
        rect = pygame.Rect(self.x,self.y,self.size,self.size)
        if self.alive:
            pygame.draw.rect(screen, (0,0,0), rect)
        else:
            pygame.draw.rect(screen, (255,255,255), rect)
        pygame.display.update()
        
pygame.init()
screen = pygame.display.set_mode((screenheight,screenwidth))
pygame.display.set_caption("Conway's Game of Life")
grid = []
cellx = 0
celly = 0
for a in range(gridwidth):
    row=[]
    for b in range(gridheight):
        row.append(cell(cellx, celly, False, cellsize))
        cellx = cellx+cellsize
    grid.append(row)
    cellx = 0
    celly = celly+cellsize
clock = pygame.time.Clock()
prevtime = time.time()
for rownum in range(len(grid)):
    row = grid[rownum]
    for cellnum in range(len(row)):
        cell = row[cellnum]
        try:
            cell.neighbors.append(grid[rownum-1][cellnum-1])
        except:
            pass
        try:
            cell.neighbors.append(grid[rownum-1][cellnum])
        except:
            pass
        try:
            cell.neighbors.append(grid[rownum-1][cellnum+1])
        except:
            pass
        try:
            cell.neighbors.append(grid[rownum][cellnum-1])
        except:
            pass
        try:
            cell.neighbors.append(grid[rownum][cellnum+1])
        except:
            pass
        try:
            cell.neighbors.append(grid[rownum+1][cellnum-1])
        except:
            pass
        try:
            cell.neighbors.append(grid[rownum+1][cellnum])
        except:
            pass
        try:
            cell.neighbors.append(grid[rownum+1][cellnum+1])
        except:
            pass
print("done")
spacehasbeenpressed = False
firsttime=True
while True:
    if ((time.time() - prevtime) >= 0) and spacehasbeenpressed:
        for row in grid:
            for cell in row:
                executerules(cell)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if pygame.key.name(event.key) == "space":
                            spacehasbeenpressed = False
        for row in grid:
            for cell in row:
                if not firsttime:
                    if cell.exempt:
                        if not cell.alive:
                            cell.alive = True
                            cell.redraw()
                    else:
                        if cell.alive:
                            cell.alive = False
                            cell.redraw()
                cell.exempt = False
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if pygame.key.name(event.key) == "space":
                            spacehasbeenpressed = False
        firsttime=False
        prevtime=time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "space":
            spacehasbeenpressed = True
        if not pygame.mouse.get_pressed()[0]:
            for row in grid:
                for cell in row:
                    cell.toggled = False
        if pygame.mouse.get_pressed()[0]:
            mousex, mousey = pygame.mouse.get_pos()
            for row in grid:
                for cell in row:
                    if ((mousex <= cell.x + cellsize) and (mousex >= cell.x)) and ((mousey <= cell.y + cellsize) and (mousey >= cell.y)) and not cell.toggled:
                        cell.alive = not cell.alive
                        cell.toggled = True
                        firsttime = True
                        cell.redraw()
    
                    