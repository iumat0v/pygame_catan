'''import pygame
import sys
import os
import random
import pygame_gui
from constants import *'''
from classes import *
from functions import *
'''pygame.init()
size = (701, 701)
screen = pygame.display.set_mode(size)'''


'''def terminate():
    pygame.quit()
    sys.exit()


def exit(manager):
    dialog = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect(250, 250, 300, 300),
        manager=manager,
        window_title="Подтверждение выхода",
        action_long_desc="Вы действительно хотите выйти?",
        action_short_name="Ok",
        blocking=True
    )


def show_text(screen, tex, pos):
    color = (0, 0, 0)
    if tex in "68":
        color = (255, 0, 0)
    font = pygame.font.Font(None, 30)
    text = font.render(tex, 1, color)
    screen.blit(text, pos)


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


def start_screen(screen):
    manager = pygame_gui.UIManager(size)
    fon = load_image("fon.jpg", size)
    screen.blit(fon, (0, 0))
    switch_start = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, size[1] - 110), (150, 50)),
        text="Старт",
        manager=manager
    )
    switch_exit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, size[1] - 60), (150, 50)),
        text="Выход из игры",
        manager=manager
    )
    while True:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(manager)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    terminate()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == switch_start:
                        return
                    if event.ui_element == switch_exit:
                        exit(manager)

            manager.process_events(event)
        screen.blit(fon, (0, 0))
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pass


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

class Tile(pygame.sprite.Sprite):
    def __init__(self, type1, pos_x, pos_y):
        super().__init__(tile_group)
        self.image = tile_images[type1]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class Board:
    def __init__(self):
        self.board = self.create_bord()
        self.cell_size = CELL_SIZE
        self.lis_c_coords = [[0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0]]
        self.crossroad_coords = set()

    def create_bord(self):
        a = [[0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0]]
        b = ["Глинянный карьер"] * 3 + ["Гора"] * 3 + ["Лес", "Пашня", "Луг"] * 4
        c = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        for y in range(len(a)):
            for x in range(len(a[y])):
                if not (x == 2 and y == 2):
                    k = len(b) - 1
                    a[y][x] = b.pop(random.randint(0, k)), c.pop(random.randint(0, k))
        return a

    def render(self, screen, player_roads, bot_roads, player_construction, player_i, bot_construction, bot_i):
        a = self.cell_size
        w = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                x0 = size[0] * 0.5 - (len(self.board[y]) * a * 1.73) / 2 + 20 + x * a * 1.73 - 20
                y0 = size[1] / 4 + a * 1.5 * y - 20
                if x == 2 and y == 2:
                    type1 = "Пустыня"
                else:
                    type1 = self.board[y][x][0]
                Tile(type1, int(x0 - a / 2), int(y0 - a + 3))
                r = (1.73 * a) / 2
                if x != 2 or y != 2:
                    w.append([str(self.board[y][x][1]), (int(x0 + r + 1), int(y0 + r / 1.73 + 2))])
                p1 = (x0, y0)
                p2 = (x0 + (a * 1.73 / 2), y0 - a / 2)
                p3 = (x0 + a * 1.73, y0)
                p4 = (x0 + a * 1.73, y0 + a)
                p5 = (x0 + (a * 1.73 / 2), y0 + (3 * a) / 2)
                p6 = (x0, y0 + a)
                #r = (1.73 * a) / 2
                if len(self.lis_c_coords) < 19:
                    self.lis_c_coords[y][x] = (x0 + r + 1, y0 + r / 1.73 + 2)
                for point in [p1, p2, p3, p4, p5, p6]:
                    self.crossroad_coords.add(point)
        tile_group.draw(screen)
        for el in w:
            show_text(screen, el[0], el[1])
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
    # __________________________________________________________________
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
                    if int(x1) != int(x) or int(y) != int(y1):
                        a.append((x, y))
        else:
            pass
        return a


class GameBot(Player):
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
        self.mast = []

    def build_settlement(self, player_construction, board: Board, start=False):
        a = self.when_build_settlement(player_construction, board.crossroad_coords, start)
        b = []
        if start:
            for crossroad in a:
                tile = {
                    "Глинянный карьер": 0,
                    "Гора": 0,
                    "Лес": 0,
                    "Пашня": 0,
                    "Луг": 0
                }
                x1, y1 = crossroad
                prior = 0
                for cell in board.lis_c_coords:
                    for x, y in cell:
                        if (x - x1) ** 2 + (y - y1) ** 2 <= CELL_SIZE ** 2 * 1.21:
                            x, y = board.get_cell((x, y))
                            if board.board[y][x] == 0:
                                continue
                            prior += VER[str(board.board[y][x][1])] / 1.5
                            if tile[board.board[y][x][0]] == 0:
                                prior += 4
                            elif tile[board.board[y][x][0]] == 1:
                                prior += 0
                            elif tile[board.board[y][x][0]] == 2:
                                prior += -3
                            tile[board.board[y][x][0]] += 1
                    b.append((crossroad, prior))
            b = sorted(b, key=lambda x: x[1], reverse=True)
            print("b:", b)
            self.list_settlements.append(b[0][0])
            self.win_points += 1
        else:
            pass

    def build_road(self, player_roads, list_crossroad_coord, start=False):
        a = self.when_build_road(player_roads, list_crossroad_coord, start)
        if start:
            print(self.list_settlements)
            x0, y0 = self.list_settlements[0]
            x1, y1 = self.list_settlements[-1]
            b = []
            for x, y in a:
                prior = 0
                if x0 <= x <= x1 or x0 >= x >= x1:
                    prior += 1
                if y0 <= y <= y1 or y0 >= y >= y1:
                    prior += 1
                b.append([(x, y), prior])
            b = sorted(b, key=lambda x: x[1], reverse=True)
            self.roads.append([(x1, y1), (x, y)])
        else:
            pass

'''
class Game:
    def __init__(self):
        self.turn = 0
        # self.step = 0
        self.board = Board()
        self.player = Player()
        self.bot = GameBot()
        self.getting_res = True
        self.trading = False
        self.building = False
        self.starting = True
        self.start_step = 0

    def play(self, pos=None, event=None):
        global TEXT
        if self.turn == 0:
            if self.getting_res:
                a = random.randint(1, 6)
                a += random.randint(1, 6)
                self.player.get_res(a, self.board)
                self.bot.get_res(a, self.board)
                self.getting_res = False
                self.trading = True
                TEXT = "Фаза торговли"
                return
            if self.trading:
                self.trading = False
                self.building = True
                TEXT = "Фаза строительства"
                return
            if self.building:
                self.building = False
                self.getting_res = True
                pass
        else:
            self.turn = 0

    def start(self, pos):
        global TEXT
        if self.start_step == 0:
            if self.player.build_settlement([], self.board, pos, self.starting):
                self.start_step += 1
                TEXT = " Вы строите дорогу"
                return
        if self.start_step == 1:
            if self.player.build_road([], self.board.crossroad_coords, pos, self.starting):
                self.start_step += 1
        self.turn = 1
        for i in range(2):
            if self.start_step == 2 + i * 2:
                self.bot.build_settlement(self.player.list_settlements, self.board, self.starting)
                self.start_step += 1
            if self.start_step == 3 + i * 2:
                self.bot.build_road([], self.board.crossroad_coords, self.starting)
                self.start_step += 1
        self.turn = 0
        if self.start_step == 6:
            TEXT = " Вы строите поселение"
            if self.player.build_settlement(self.bot.list_settlements, self.board, pos, self.starting):
                self.start_step += 1
                TEXT = " Вы строите дорогу"
                return
        if self.start_step == 7:
            if self.player.build_road(self.bot.roads, self.board.crossroad_coords, pos, self.starting):
                self.start_step += 1
                self.starting = False
                TEXT = ""

    def render(self, screen):
        pr, br = self.player.roads, self.bot.roads
        pc = self.player.list_settlements + self.player.list_cities
        bc = self.bot.list_settlements + self.bot.list_cities
        pi, bi = len(self.player.list_settlements), len(self.bot.list_settlements)
        self.board.render(screen, pr, br, pc, pi, bc, bi)


pygame.display.set_caption("Catan")
clock = pygame.time.Clock()
start_screen(screen)
game = Game()
screen.fill((0, 0, 255))
run = True
manager = pygame_gui.UIManager(size)
# ---------------------------
label1 = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, size[1] - 70, 150, 60),
    text='Player1',
    manager=manager
)
label2 = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(0, 0, 180, 100),
    text='Bot',
    manager=manager
)
btn_road = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(size[0] - 215, size[1] - 165, 170, 40),
    text="Построить",
    manager=manager
)
btn_settlement = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(size[0] - 135, size[1] - 128, 100, 40),
    text="Построить",
    manager=manager
)
btn_city = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(size[0] - 120, size[1] - 93, 100, 35),
    text="Построить",
    manager=manager
)
btn_cards = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(size[0] - 180, size[1] - 60, 150, 45),
    text="Построить",
    manager=manager
)
im_rect_player1 = load_image("Прямоугольник.png", (150, 60))
im_rect_bot = load_image("ПрямоугольникBot.png", (180, 100))
im_cost = load_image("cost1.png", (370, 200), colorkey=-1)
im_scroll = load_image("свиток.png", (size[0] // 2, 130), colorkey=-1)
icon_c = load_image("clay_icon.png", (50, 50), colorkey=-1)
icon_s = load_image("sheep_icon.png", (50, 50), colorkey=-1)
icon_st = load_image("stone_icone.png", (50, 50))
icon_wh = load_image("wheat_icon.jpg", (50, 50))
icon_w = load_image("wood_icon.png", (50, 50))
icons = [icon_c, icon_st, icon_w, icon_wh, icon_s]
# ------------------------------

while run:
    time_delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(manager)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.starting:
                game.start(event.pos)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                terminate()
        manager.process_events(event)
    if not game.starting:
        game.play()
    screen.fill((0, 0, 255))
    # ---------------
    screen.blit(im_rect_player1, (10, size[1] - 70))
    screen.blit(im_cost, (size[0] - 370, size[1] - 200))
    screen.blit(im_rect_bot, (3, 0))
    screen.blit(im_scroll, (size[0] // 4, 0))
    a = list(game.player.res.values())
    for i in range(len(icons)):
        screen.blit(icons[i], (60 * i, size[1] - 175))
        show_text(screen, str(a[i]), (60 * i + 25, size[1] - 120))
    show_text(screen, TEXT, (size[0] // 4 + 60, 50), color=(50, 50, 50))
    show_text(screen, TITLE, (size[0] * 4 // 9, 30))
    # ---------------
    game.render(screen)
    manager.update(time_delta)
    manager.draw_ui(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()