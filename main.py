import pygame
import sys
import os
import random


pygame.init()
size = (601, 601)
screen = pygame.display.set_mode(size)


def load_image(name, size, angle=0, colorkey=None, direct="images"):
    fullname = os.path.join(direct, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image = pygame.transform.scale(image, size)
    image = pygame.transform.rotate(image, angle)
    return image

cell_size = 50
tile_images = {
    "Глинянный карьер": load_image("Глинянный карьер.png", (cell_size * 2, cell_size * 2), 30, - 1),
    "Гора": load_image("Гора.png", (cell_size * 2, cell_size * 2), 30, - 1),
    "Лес": load_image("Лес.png", (cell_size * 2, cell_size * 2), 30, - 1),
    "Пашня": load_image("Пашня.png", (cell_size * 2, cell_size * 2), 30, - 1),
    "Пустыня": load_image("Пустыня.png", (cell_size * 2, cell_size * 2), 30, - 1),
    "Луг": load_image("Луг.png", (cell_size * 2, cell_size * 2), 30, - 1)
}
tile_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, type1, pos_x, pos_y):
        super().__init__(tile_group)
        self.image = tile_images[type1]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class Board:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0]]
        b = ["Глинянный карьер"] * 3 + ["Гора"] * 3 + ["Лес", "Пашня", "Луг"] * 4
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if not (x == 2 and y == 2):
                    self.board[y][x] = b.pop(random.randint(0, len(b) - 1))
        self.cell_size = cell_size
        self.lis_c_coords = [[0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0]]
        self.crossroad_coords = set()

    def render(self, screen):
        a = self.cell_size
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                x0 = int(size[0] * 0.5) - (len(self.board[y]) * a * 1.73) // 2 + 20 + int(x * a * 1.73) - 20
                y0 = size[1] // 4 + int(a * 1.5) * y - 20
                if x == 2 and y == 2:
                    type1 = "Пустыня"
                else:
                    type1 = self.board[y][x]
                Tile(type1, x0 - a // 2, y0 - a + 3)
                p1 = (x0, y0)
                p2 = (x0 + (a * 1.73 // 2), y0 - a // 2)
                p3 = (int(x0 + a * 1.73), y0)
                p4 = (int(x0 + a * 1.73), y0 + a)
                p5 = (x0 + (a * 1.73 // 2), y0 + (3 * a) // 2)
                p6 = (x0, y0 + a)
                r = (1.73 * a) // 2
                tile_group.draw(screen)
                if len(self.lis_c_coords) < 19:
                    self.lis_c_coords[y][x] = (x0 + r + 1, y0 + int(r / 1.73) + 2)
                for point in [p1, p2, p3, p4, p5, p6]:
                    self.crossroad_coords.add(point)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        xm, ym = mouse_pos
        r = (1.73 * self.cell_size) // 2
        for y in range(len(self.lis_c_coords)):
            for x in range(len(self.lis_c_coords[y])):
                xc, yc = self.lis_c_coords[y][x]
                d = ((xc - xm) ** 2 + (yc - ym) ** 2) ** 0.5
                if d <= r:
                    return (x, y)
        return None

    def on_click(self, cell_coords):
        print(cell_coords)


board = Board()
screen.fill((0, 0, 255))
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    board.render(screen)
    pygame.display.flip()
pygame.quit()