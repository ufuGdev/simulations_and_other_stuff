import pygame
import numpy as np
import random

GRID_WIDTH = 150
GRID_HEIGHT = 150
CELL_SIZE = 6
EMPTY = 0
SAND = 1
WATER = 2
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BUTTON_COLOR = (200, 200, 200)


pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE + 50))  
clock = pygame.time.Clock()
pygame.display.set_caption("Kum ve Su Simülasyonu")
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
current_material = SAND  
mouse_held = False  

class Button:
    def __init__(self, x, y, width, height, color, text, text_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

sand_button = Button(10, 10, 100, 30, YELLOW, "Kum", BLACK, SAND)
water_button = Button(120, 10, 100, 30, BLUE, "Su", WHITE, WATER)
buttons = [sand_button, water_button]

def add_material(mouse_x, mouse_y):
    grid_x = mouse_x // CELL_SIZE
    grid_y = (mouse_y - 50) // CELL_SIZE  # Üst kısımdaki butonları hesaba kat
    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
        grid[grid_y, grid_x] = current_material
def update_grid():
    for y in range(GRID_HEIGHT - 2, -1, -1):  # Alttan üste doğru
        for x in range(GRID_WIDTH):
            if grid[y, x] == SAND:
                if grid[y + 1, x] == EMPTY:  # Kum düz aşağı düşer
                    grid[y, x], grid[y + 1, x] = EMPTY, SAND
                elif x > 0 and grid[y + 1, x - 1] == EMPTY:  # Sol çapraz
                    grid[y, x], grid[y + 1, x - 1] = EMPTY, SAND
                elif x < GRID_WIDTH - 1 and grid[y + 1, x + 1] == EMPTY:  # Sağ çapraz
                    grid[y, x], grid[y + 1, x + 1] = EMPTY, SAND
                elif grid[y + 1, x] == WATER:  # Su ile yer değiştir
                    grid[y, x], grid[y + 1, x] = WATER, SAND
def update_grid():
    for y in range(GRID_HEIGHT - 2, -1, -1):  # Alttan üste doğru
        for x in range(GRID_WIDTH):
            if grid[y, x] == SAND:
                # Kumun hareketi
                if grid[y + 1, x] == EMPTY:  # Kum düz aşağı düşer
                    grid[y, x], grid[y + 1, x] = EMPTY, SAND
                elif x > 0 and grid[y + 1, x - 1] == EMPTY:  # Sol çapraz
                    grid[y, x], grid[y + 1, x - 1] = EMPTY, SAND
                elif x < GRID_WIDTH - 1 and grid[y + 1, x + 1] == EMPTY:  # Sağ çapraz
                    grid[y, x], grid[y + 1, x + 1] = EMPTY, SAND
                elif grid[y + 1, x] == WATER:  # Su ile yer değiştir
                    grid[y, x], grid[y + 1, x] = WATER, SAND
            elif grid[y, x] == WATER:
                # Suyun hareketi
                if grid[y + 1, x] == EMPTY:  # Su düz aşağı düşer
                    grid[y, x], grid[y + 1, x] = EMPTY, WATER
                else:
                    left_empty = x > 0 and grid[y, x - 1] == EMPTY  # Sol boş mu?
                    right_empty = x < GRID_WIDTH - 1 and grid[y, x + 1] == EMPTY  # Sağ boş mu?

                    if left_empty and right_empty:  # İki taraf da boşsa rastgele birini seç
                        if random.choice([True, False]):  # %50 ihtimalle sola veya sağa git
                            grid[y, x], grid[y, x - 1] = EMPTY, WATER
                        else:
                            grid[y, x], grid[y, x + 1] = EMPTY, WATER
                    elif left_empty:  # Sadece sol boşsa sola git
                        grid[y, x], grid[y, x - 1] = EMPTY, WATER
                    elif right_empty:  # Sadece sağ boşsa sağa git
                        grid[y, x], grid[y, x + 1] = EMPTY, WATER
def draw_grid():
    screen.fill(BLACK)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x] == SAND:
                pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE, y * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))
            elif grid[y, x] == WATER:
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))
def draw_buttons():
    for button in buttons:
        button.draw(screen)
        
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_held = True
            for button in buttons:
                if button.is_clicked((mouse_x, mouse_y)):
                    current_material = button.action
            if mouse_y > 50:  
                add_material(mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False
    if mouse_held:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 50:  # Butonların altındaki alana tıklanıyorsa
            add_material(mouse_x, mouse_y)

    update_grid()
    draw_grid()
    draw_buttons()
    pygame.display.flip()
    clock.tick(150)

pygame.quit()
