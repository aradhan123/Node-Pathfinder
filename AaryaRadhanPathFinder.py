#Aarya Radhan Pathfinder

import pygame
from queue import PriorityQueue
import math
import time

w = 600
W = pygame.display.set_mode((w, w))
pygame.display.set_caption("Path Finder")

R = (200, 0, 0)       
g = (0, 200, 0)       
b = (0, 0, 255)      
y = (255, 215, 0)     
wh = (245, 245, 245)  
bl = (50, 50, 50)     
p = (148, 0, 211)     
o = (255, 140, 0)
grey = (128, 128, 128)
t = (72, 209, 204)  

class Spot:
    def __init__(self, r, c, wi, tr):
        self.r = r
        self.c = c
        self.wi = wi
        self.tr = tr
        self.x = r * wi
        self.y = c * wi
        self.color = wh
        self.neighbors = []

    def get_pos(self):
        return self.r, self.c

    def is_closed(self):
        return self.color == R

    def is_open(self):
        return self.color == g

    def is_barrier(self):
        return self.color == bl

    def is_start(self):
        return self.color == o

    def is_end(self):
        return self.color == t

    def reset(self):
        self.color = wh

    def make_start(self):
        self.color = o

    def make_closed(self):
        self.color = R

    def make_open(self):
        self.color = g

    def make_barrier(self):
        self.color = bl

    def make_end(self):
        self.color = t

    def make_path(self):
        self.color = p

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.wi, self.wi))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.r < self.tr - 1 and not grid[self.r + 1][self.c].is_barrier():  
            self.neighbors.append(grid[self.r + 1][self.c])

        if self.r > 0 and not grid[self.r - 1][self.c].is_barrier():  
            self.neighbors.append(grid[self.r - 1][self.c])

        if self.c < self.tr - 1 and not grid[self.r][self.c + 1].is_barrier():  
            self.neighbors.append(grid[self.r][self.c + 1])

        if self.c > 0 and not grid[self.r][self.c - 1].is_barrier():  
            self.neighbors.append(grid[self.r][self.c - 1])

    #Diagonal neighbors
        if self.r < self.tr - 1 and self.c < self.tr - 1 and not grid[self.r + 1][self.c + 1].is_barrier():
            self.neighbors.append(grid[self.r + 1][self.c + 1])

        if self.r > 0 and self.c > 0 and not grid[self.r - 1][self.c - 1].is_barrier():
            self.neighbors.append(grid[self.r - 1][self.c - 1])

        if self.r < self.tr - 1 and self.c > 0 and not grid[self.r + 1][self.c - 1].is_barrier():
            self.neighbors.append(grid[self.r + 1][self.c - 1])

        if self.r > 0 and self.c < self.tr - 1 and not grid[self.r - 1][self.c + 1].is_barrier():
            self.neighbors.append(grid[self.r - 1][self.c + 1])


    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    start_time = time.time() 

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            end_time = time.time()  
            print(f"Path found in {end_time - start_time:.2f} seconds")
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    end_time = time.time()  
    print(f"No path found. Time elapsed: {end_time - start_time:.2f} seconds")
    return False

def make_grid(r, wi):
    grid = []
    gap = wi // r
    for i in range(r):
        grid.append([])
        for j in range(r):
            spot = Spot(i, j, gap, r)
            grid[i].append(spot)
    return grid

def draw_grid(window, r, wi):
    gap = wi // r
    for i in range(r):
        pygame.draw.line(window, grey, (0, i * gap), (wi, i * gap))
        for j in range(r):
            pygame.draw.line(window, grey, (j * gap, 0), (j * gap, wi))

def draw(window, grid, r, wi):
    window.fill(wh)

    for row in grid:
        for spot in row:
            spot.draw(window)

    draw_grid(window, r, wi)
    pygame.display.update()

def get_clicked_pos(pos, r, wi):
    gap = wi // r
    y, x = pos

    r = y // gap
    c = x // gap

    return r, c

def main(window, wi):
    ROWS = 50
    grid = make_grid(ROWS, wi)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(window, grid, ROWS, wi)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  
                pos = pygame.mouse.get_pos()
                r, c = get_clicked_pos(pos, ROWS, wi)
                spot = grid[r][c]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  
                pos = pygame.mouse.get_pos()
                r, c = get_clicked_pos(pos, ROWS, wi)
                spot = grid[r][c]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(window, grid, ROWS, wi), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, wi)

    pygame.quit()

main(W, w)
