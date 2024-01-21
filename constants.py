import pygame
from functions import load_image

CELL_SIZE = 45
tile_images = {
    "Глинянный карьер": load_image("Глинянный карьер.png", (CELL_SIZE * 2, CELL_SIZE * 2), 30, - 1),
    "Гора": load_image("Гора.png", (CELL_SIZE * 2, CELL_SIZE * 2), 30, - 1),
    "Лес": load_image("Лес.png", (CELL_SIZE * 2, CELL_SIZE * 2), 30, - 1),
    "Пашня": load_image("Пашня.png", (CELL_SIZE * 2, CELL_SIZE * 2), 30, - 1),
    "Пустыня": load_image("Пустыня.png", (CELL_SIZE * 2, CELL_SIZE * 2), 30, - 1),
    "Луг": load_image("Луг.png", (CELL_SIZE * 2, CELL_SIZE * 2), 30, - 1)
}
tile_group = pygame.sprite.Group()
VER = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "8": 5,
    "9": 4,
    "10": 3,
    "11": 2,
    "12": 1
}
size = (701, 701)
FPS = 10
TITLE = "Старт"
TEXT = " Вы строите поселение"
EVENT = None
PRODUCT1 = "Лес"
PRODUCT2 = "Лес"
res_tile = {
    "Лес": "Лес",
    "Пшеница": "Пашня",
    "Глина": "Глинянный карьер",
    "Камень": "Гора",
    "Овцы": "Луг"
}
