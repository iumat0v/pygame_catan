import pygame
import sys
import os
import random

pygame.init()
size = (701, 701)
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

        self.cell_size = CELL_SIZE
        self.lis_c_coords = [[0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0]]
        self.crossroad_coords = set()

    def render(self, screen, player_roads, bot_roads, player_construction, player_i, bot_construction, bot_i):
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
                if len(self.lis_c_coords) < 19:
                    self.lis_c_coords[y][x] = (x0 + r + 1, y0 + int(r / 1.73) + 2)
                for point in [p1, p2, p3, p4, p5, p6]:
                    self.crossroad_coords.add(point)
        tile_group.draw(screen)
        for settlement in player_construction[:player_i]:
            pygame.draw.circle(screen, (255, 0, 0), settlement, CELL_SIZE // 4)
        for citi in player_construction[player_i:]:
            pygame.draw.circle(screen, (255, 0, 0), citi, CELL_SIZE // 3)
        for settlement in bot_construction[:bot_i]:
            pygame.draw.circle(screen, (0, 0, 255), settlement, CELL_SIZE // 4)
        for citi in bot_construction[bot_i:]:
            pygame.draw.circle(screen, (0, 0, 255), citi, CELL_SIZE // 3)
        for point1, point2 in player_roads:
            pygame.draw.line(screen, (255, 0, 0), point1, point2, 5)
        for point1, point2 in bot_roads:
            pygame.draw.line(screen, (0, 0, 255), point1, point2, 5)
    # __________________________________________________________________-
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
    # _____________________________________________________


class Player:
    def __init__(self):
        self.wood = 0
        self.stone = 0
        self.clay = 0
        self.wheat = 0
        self.sheep = 0
        self.win_points = 0
        self.list_settlements = []
        self.list_cities = []
        self.roads = []

    def build_settlement(self, bot_construction, list_crossroad_coord, pos, start=False):
        a = self.when_build_settlement(bot_construction, list_crossroad_coord, start)
        if start:
            for x, y in a:
                if (pos[0] - x) ** 2 + (pos[1] - y) ** 2 <= CELL_SIZE ** 2 // 9:
                    self.list_settlements.append((x, y))
                    self.win_points += 1
                    print(self.win_points)
                    return True
        else:
            pass

    def build_road(self, bot_roads, list_crossroad_coord, pos, start=False):
        a = self.when_build_road(bot_roads, list_crossroad_coord, start)
        if start:
            for x, y in a:
                if (pos[0] - x) ** 2 + (pos[1] - y) ** 2 <= CELL_SIZE ** 2 // 1.21:
                    self.roads.append([self.list_settlements[-1], (x, y)])
                    return True
        else:
            pass

    def when_build_settlement(self, bot_construction, list_crossroad_coord, start=False):
        construction = bot_construction + self.list_settlements + self.list_cities
        a = []
        if start:
            for x, y in list_crossroad_coord:
                for x1, y1 in construction:
                    if (x - x1) ** 2 + (y - y1) ** 2 <= CELL_SIZE ** 2 * 1.21:
                        break
                else:
                    a.append((x, y))
        else:
            pass
        return a

    def when_build_road(self, bot_roads, list_crossroad_coord, start=False):
        a = []
        if start:
            x1, y1 = self.list_settlements[-1]
            for x, y in list_crossroad_coord:
                if (x - x1) ** 2 + (y - y1) ** 2 <= CELL_SIZE ** 2:
                    if x1 != x or y != y1:
                        a.append((x, y))
        else:
            pass
        return a


class GameBot:
    def __init__(self):
        self.wood = 0
        self.stone = 0
        self.clay = 0
        self.wheat = 0
        self.sheep = 0
        self.win_points = 0
        self.list_settlements = []
        self.list_cities = []
        self.roads = []

    def build_settlement(self, player_construction, list_crossroad_coord, start=False):
        if start:
            pass
        else:
            pass

    def build_road(self, player_roads, list_crossroad_coord, start=False):
        if start:
            pass
        else:
            pass

    def when_build_settlement(self, player_construction, list_crossroad_coord, start=False):
        construction = player_construction + self.list_settlements + self.list_cities
        a = []
        if start:
            for x, y in list_crossroad_coord:
                for x1, y1 in construction:
                    if (x - x1) ** 2 + (y - y1) ** 2 <= CELL_SIZE ** 2:
                        break
                else:
                    a.append((x, y))
        else:
            pass
        return a

    def when_build_road(self, player_roads, list_crossroad_coord, start=False):
        a = []
        if start:
            x1, y1 = self.list_settlements[-1]
            for x, y in list_crossroad_coord:
                if (x - x1) ** 2 + (y - y1) ** 2 <= CELL_SIZE ** 2:
                    if x1 != x or y != y1:
                        a.append((x, y))
        else:
            pass
        return a
        pass


class Game:
    def __init__(self):
        self.turn = 0
        self.board = Board()
        self.player = Player()
        self.bot = GameBot()
        self.getting_res = False
        self.trading = False
        self.building = False
        self.starting = True
        self.start_step = 0

    def play(self):
        pass

    def start(self, pos):

        if self.start_step == 0:
            if self.player.build_settlement([], self.board.crossroad_coords, pos, self.starting):
                self.start_step += 1
                return
        if self.start_step == 1:
            if self.player.build_road([], self.board.crossroad_coords, pos, self.starting):
                self.start_step += 1
        for i in range(2):
            if self.start_step == 2 + i * 2:
                self.bot.build_settlement(self.player.list_settlements, self.board.crossroad_coords, self.starting)
                self.start_step += 1
            if self.start_step == 3 + i * 2:
                self.bot.build_road([], self.board.crossroad_coords, self.starting)
                self.start_step += 1
        if self.start_step == 6:
            if self.player.build_settlement(self.bot.list_settlements, self.board.crossroad_coords, pos, self.starting):
                self.start_step += 1
                return
        if self.start_step == 7:
            if self.player.build_road(self.bot.roads, self.board.crossroad_coords, pos, self.starting):
                self.start_step += 1
                self.starting = False

    def render(self, screen):
        pr, br = self.player.roads, self.bot.roads
        pc = self.player.list_settlements + self.player.list_cities
        bc = self.bot.list_settlements + self.bot.list_cities
        pi, bi = len(self.player.list_settlements), len(self.bot.list_settlements)
        self.board.render(screen, pr, br, pc, pi, bc, bi)


game = Game()
screen.fill((0, 0, 255))
run = True
clock = pygame.time.Clock()
FPS = 2

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.starting:
                game.start(event.pos)
    game.render(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
