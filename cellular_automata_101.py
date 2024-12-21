import pygame
import numpy as np

GRID_WIDTH = 200
GRID_HEIGHT = 200
CELL_SIZE = 5
FPS = 10

RULE = 50 # tek boyutlu Cellular Automata kuralnı burada belirle
""" 
(https://mathworld.wolfram.com/ElementaryCellularAutomaton.html) bu sitedekine göre renkler tam tersi olacak
alttaki değişkenlerin ismini değişerek değiştirebilirisin görüntüyü. normalde renk atamaları yanlış olur ama tüm kodu düzelltmektense böyle daha basit
"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cellular Automata")
clock = pygame.time.Clock()

def draw_grid(grid):

    screen.fill(BLACK)
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 1:
                pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
def grid_init():
    """
    Belirlenen ölçüde bir canvas oluşturup on yukarı ortadaki hücreyi 1 yapar.
    """
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    grid[0, GRID_WIDTH // 2] = 1
    return grid

def rules(left, center, right):
    """
    girilen sayıyı binary çevirerek 8 bite sığdırıp kuralı belirler
    """
    binary = [int(x) for x in bin(RULE)[2:].zfill(8)]
    if left == 1 and center == 1 and right == 1:
        return binary[0]
    elif left == 1 and center == 1 and right == 0:
        return binary[1]
    elif left == 1 and center == 0 and right == 1:
        return binary[2]
    elif left == 1 and center == 0 and right == 0:
        return binary[3]
    elif left == 0 and center == 1 and right == 1:
        return binary[4]
    elif left == 0 and center == 1 and right == 0:
        return binary[5]
    elif left == 0 and center == 0 and right == 1:
        return binary[6]
    elif left == 0 and center == 0 and right == 0:
        return binary[7]

    return 0
def update_row(previous_row):
    new_row = np.zeros_like(previous_row)
    for col in range(len(previous_row)):
        left = previous_row[(col - 1) % len(previous_row)]
        center = previous_row[col]
        right = previous_row[(col + 1) % len(previous_row)]
        new_row[col] = rules(left, center, right)

    return new_row

def main():
    grid = grid_init()

    running = True
    for row in range(1, GRID_HEIGHT):
        grid[row] = update_row(grid[row - 1])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid(grid)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
