import numpy as np
import pygame as pg
import random

pg.init()
WIDTH, HEIGHT = 800, 800
BACKGROUND = (0, 0, 0)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Random Walker")
clock = pg.time.Clock()

def draw_grid(grid):

    screen.fill(BACKGROUND)
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 1:
                color = (255, 255, 255)
                pg.draw.rect(screen, color, (col * 10, row * 10, 10, 10))

def grid_init():

    grid = np.zeros((HEIGHT // 10, WIDTH // 10), dtype=int)
    grid[grid.shape[0] // 2, grid.shape[1] // 2] = 1
    return grid

def update_grid(grid, pos):

    row, col = pos
    dr,dc=0,0
    diff= [-1,0,1,0]
    dr = random.choice(diff)
    new_row = (row + dr) % grid.shape[0]
    if row== new_row:
        dc = random.choice(diff)
    new_col = (col + dc) % grid.shape[1]
    grid[new_row, new_col] = 1
    return grid, (new_row, new_col)

def main():
    grid = grid_init()
    pos = (grid.shape[0] // 2, grid.shape[1] // 2)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        grid,pos = update_grid(grid,pos)
        draw_grid(grid)
        pg.display.flip()
        clock.tick(30)

    pg.quit()
if __name__ == "__main__":
    main()
    