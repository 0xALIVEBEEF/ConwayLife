import pygame

x = None
y = None
alive = None
cellindex = None
alives = None
index = None
enabled = None
cellsx = None
neighbors = None
cellpos = None
counter = None
cellsy = None
cellposx = None
i = None
cellalive = None
cellsize = None
factors = None
numcells = None
cellposy = None
alivecells = None
alivenextcells = None
touchy = None
toggledcells = None
touchx = None
k = None
specificcell = None
aliveneighbors = None
m = None
placeholder = None

def first_index(my_list, elem):
  try: index = my_list.index(elem) + 1
  except: index = 0
  return index

def upRange(start, stop, step):
  while start <= stop:
    yield start
    start += abs(step)

def downRange(start, stop, step):
  while start >= stop:
    yield start
    start -= abs(step)

def drawcells():
  global x, y, alive, cellindex, alives, index, enabled, cellsx, neighbors, cellpos, counter, cellsy, cellposx, i, cellalive, cellsize, factors, numcells, cellposy, alivecells, alivenextcells, touchy, toggledcells, touchx, k, specificcell, aliveneighbors, m, placeholder
  cellsx = width / cellsize
  cellsy = height / cellsize
  numcells = cellsx * cellsy
  alivecells = [False] * int(numcells)
  alivenextcells = [False] * int(numcells)

def findcell(x, y):
  global alive, cellindex, alives, index, enabled, cellsx, neighbors, cellpos, counter, cellsy, cellposx, i, cellalive, cellsize, factors, numcells, cellposy, alivecells, alivenextcells, touchy, toggledcells, touchx, k, specificcell, aliveneighbors, m, placeholder
  if x > width or y > height or x < 0 or y < 0:
    return 0
  cellposx = (x - x % cellsize) / cellsize
  cellposy = (y - y % cellsize) / cellsize
  return cellposx + cellposy * cellsx

def drawcell(x, y, alive):
  global cellindex, alives, index, enabled, cellsx, neighbors, cellpos, counter, cellsy, cellposx, i, cellalive, cellsize, factors, numcells, cellposy, alivecells, alivenextcells, touchy, toggledcells, touchx, k, specificcell, aliveneighbors, m, placeholder
  rect = pygame.Rect(x,y,cellsize,cellsize)
  if alive:
    pygame.draw.rect(screen, (255,255,255), rect)
  else:
    pygame.draw.rect(screen, (0,0,0), rect)
  pygame.display.update()

def findneighbors(cellindex):
  global x, y, alive, alives, index, enabled, cellsx, neighbors, cellpos, counter, cellsy, cellposx, i, cellalive, cellsize, factors, numcells, cellposy, alivecells, alivenextcells, touchy, toggledcells, touchx, k, specificcell, aliveneighbors, m, placeholder
  neighbors = []
  for i in [(cellindex - width / cellsize) + 1, cellindex - width / cellsize, (cellindex - width / cellsize) - 1, cellindex + 1, cellindex - 1, (cellindex + width / cellsize) + 1, cellindex + width / cellsize, (cellindex + width / cellsize) - 1]:
    if i > 0 and i < numcells:
      neighbors.append(i)
  return neighbors

def executerules(alives, cellindex):
  global x, y, alive, index, enabled, cellsx, neighbors, cellpos, counter, cellsy, cellposx, i, cellalive, cellsize, factors, numcells, cellposy, alivecells, alivenextcells, touchy, toggledcells, touchx, k, specificcell, aliveneighbors, m, placeholder
  cellpos = findcellpos(cellindex)
  cellalive = alivecells[int(cellindex - 1)]
  if alives == 3 and not cellalive:
    drawcell(int(cellpos[0]), int(cellpos[1]), True)
    alivenextcells[int(cellindex - 1)] = True
  elif (alives == 3 or alives == 2) and cellalive:
    alivenextcells[int(cellindex - 1)] = True
  elif cellalive:
    drawcell(int(cellpos[0]), int(cellpos[1]), False)
    alivenextcells[int(cellindex - 1)] = False
  return 0

def findcellpos(index):
  global x, y, alive, cellindex, alives, enabled, cellsx, neighbors, cellpos, counter, cellsy, cellposx, i, cellalive, cellsize, factors, numcells, cellposy, alivecells, alivenextcells, touchy, toggledcells, touchx, k, specificcell, aliveneighbors, m, placeholder
  return [(index % cellsx) * cellsize, ((index - index % cellsx) / cellsx) * cellsize]


enabled = False
counter = 1
factors = [2, 4, 8, 10]
cellsize = 10
pygame.init()
height = 1000
width = 1000
screen = pygame.display.set_mode((height,width))
pygame.display.set_caption("Conway's Game of Life")
drawcells()
drawcell(0,0,True)
while True:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
            quit()
      
      if pygame.mouse.get_pressed()[0]:
          print("hi")
          touchx, touchy = pygame.mouse.get_pos()
          specificcell = findcell(touchx, touchy)
          if specificcell in toggledcells:
              
              if alivecells[int(specificcell - 1)]:
                  alivecells[int(specificcell - 1)] = False
              else:
                  alivecells[int(specificcell - 1)] = True
          drawcell(touchx - touchx % cellsize, touchy - touchy % cellsize, alivecells[int(specificcell - 1)])
          toggledcells.append(specificcell)
      else:
        toggledcells = []
  if enabled:
    k_end = float(len(alivecells))
    for k in (1 <= k_end) and upRange(1, k_end, 1) or downRange(1, k_end, 1):
      aliveneighbors = 0
      for m in findneighbors(k):
        if alivecells[int(m - 1)]:
          aliveneighbors = (aliveneighbors if isinstance(aliveneighbors, Number) else 0) + 1
      print(aliveneighbors)
      placeholder = executerules(aliveneighbors, k)
    alivecells = alivenextcells
