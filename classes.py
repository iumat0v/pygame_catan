import random
from constants import *
from functions import show_text


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
            pygame.draw.circle(screen, (0, 255, 0), settlement, CELL_SIZE // 4)
        for citi in bot_construction[bot_i:]:
            pygame.draw.circle(screen, (0, 255, 0), citi, CELL_SIZE // 3)
        for point1, point2 in player_roads:
            pygame.draw.line(screen, (255, 0, 0), point1, point2, 5)
        for point1, point2 in bot_roads:
            pygame.draw.line(screen, (0, 255, 0), point1, point2, 5)
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
    # _____________________________________________________


class Player:
    def __init__(self):
        self.res = {
                    "Глинянный карьер": 0,
                    "Гора": 0,
                    "Лес": 0,
                    "Пашня": 0,
                    "Луг": 0
                }
        self.win_points = 0
        self.list_settlements = []
        self.list_cities = []
        self.roads = []

    def build_settlement(self, bot_construction, board: Board, pos, start=False):
        a = self.when_build_settlement(bot_construction, board.crossroad_coords, start)
        if start:
            for x, y in a:
                if (pos[0] - x) ** 2 + (pos[1] - y) ** 2 <= CELL_SIZE ** 2 // 9:
                    if self.list_settlements:
                        for tile in self.near_tile((x, y), board):
                            self.res[tile[0]] += 1
                    self.list_settlements.append((x, y))
                    self.win_points += 1
                    return True
        else:
            for x, y in a:
                if (pos[0] - x) ** 2 + (pos[1] - y) ** 2 <= CELL_SIZE ** 2 // 9:
                    self.res["Глинянный карьер"] -= 1
                    self.res["Лес"] -= 1
                    self.res["Пашня"] -= 1
                    self.res["Луг"] -= 1
                    self.list_settlements.append((x, y))
                    self.win_points += 1
                    return True

    def build_road(self, bot_roads, list_crossroad_coord, pos, start=False):
        a = self.when_build_road(bot_roads, list_crossroad_coord, start=start)
        if start:
            for x, y in a:
                if (pos[0] - x) ** 2 + (pos[1] - y) ** 2 <= CELL_SIZE ** 2 // 1.21:
                    self.roads.append([self.list_settlements[-1], (x, y)])
                    return True
        else:
            x0, y0 = None, None
            b = set()
            for road in self.roads:
                b.add(road[0])
                b.add(road[1])
            for x1, y1 in b:
                if (x1 - pos[0]) ** 2 + (y1 - pos[1]) ** 2 <= CELL_SIZE ** 2 // 1.21:
                    x0, y0 = x1, y1
            a = self.when_build_road(bot_roads, list_crossroad_coord, x1=x0, y1=y0)
            for x, y in a:
                if (pos[0] - x) ** 2 + (pos[1] - y) ** 2 <= CELL_SIZE ** 2 // 1.21:
                    self.res["Глинянный карьер"] -= 1
                    self.res["Лес"] -= 1
                    self.roads.append([(x0, y0), (x, y)])
                    print("YES!")
                    return True

    def build_citi(self, pos):
        for x, y in self.list_settlements:
            if (x - pos[0]) ** 2 + (y - pos[1]) ** 2 <= CELL_SIZE ** 2 // 1.44:
                del self.list_settlements[self.list_settlements.index((x, y))]
                self.list_cities.append((x, y))
                self.win_points += 1
                self.res["Гора"] -= 3
                self.res["Пашня"] -= 2
                return True

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
            b = set()
            for road in self.roads:
                b.add(road[0])
                b.add(road[1])
            for x, y in b:
                for x1, y1 in construction:
                    if (x - x1) ** 2 + (y - y1) ** 2 < CELL_SIZE ** 2 * 1.21:
                        break
                else:
                    a.append((x, y))
        return a

    def when_build_road(self, bot_roads, list_crossroad_coord, x1=None, y1=None, start=False):
        a = []
        if start:
            x1, y1 = self.list_settlements[-1]
            for x, y in list_crossroad_coord:
                if (x - x1) ** 2 + (y - y1) ** 2 <= CELL_SIZE ** 2:
                    if int(x1) != int(x) or int(y) != int(y1):
                        a.append((x, y))
        else:
            if x1 and y1:
                for x, y in list_crossroad_coord:
                    if 0 < (x - x1) ** 2 + (y - y1) ** 2 <= CELL_SIZE ** 2:
                        b = [(x1, y1), (x, y)]
                        if (b not in (bot_roads + self.roads)) and (reversed(b) not in (bot_roads + self.roads)):
                            a.append((x, y))
        return a

    def near_tile(self, crossroad, board: Board):
        x1, y1 = crossroad
        a = []
        for cell in board.lis_c_coords:
            for x, y in cell:
                if (x - x1) ** 2 + (y - y1) ** 2 <= CELL_SIZE ** 2 * 1.21:
                    x, y = board.get_cell((x, y))
                    if board.board[y][x] == 0:
                        continue
                    else:
                        a.append(board.board[y][x])
        return a

    def get_res(self, a, board):
        for crossroad in (self.list_settlements + self.list_cities):
            for tile in self.near_tile(crossroad, board):
                if tile[1] == a:
                    if crossroad in self.list_settlements:
                        self.res[tile[0]] += 1
                    else:
                        self.res[tile[0]] += 2


class GameBot(Player):
    def __init__(self):
        self.res = {
            "Глинянный карьер": 0,
            "Гора": 0,
            "Лес": 0,
            "Пашня": 0,
            "Луг": 0
        }
        self.win_points = 0
        self.list_settlements = []
        self.list_cities = []
        self.roads = []
        self.tile = {
                    "Глинянный карьер": 0,
                    "Гора": 0,
                    "Лес": 0,
                    "Пашня": 0,
                    "Луг": 0
                }

    def build_settlement(self, player_construction, board: Board, start=False):
        a = self.when_build_settlement(player_construction, board.crossroad_coords, start)
        b = []
        if start:
            for crossroad in a:
                x1, y1 = crossroad
                prior = 0
                for cell in board.lis_c_coords:
                    for x, y in cell:
                        if (x - x1) ** 2 + (y - y1) ** 2 <= CELL_SIZE ** 2 * 1.21:
                            x, y = board.get_cell((x, y))
                            if board.board[y][x] == 0:
                                continue
                            prior += VER[str(board.board[y][x][1])] * 1.5
                            if self.tile[board.board[y][x][0]] == 0:
                                prior += 4
                            elif self.tile[board.board[y][x][0]] == 1:
                                prior += 0
                            elif self.tile[board.board[y][x][0]] == 2:
                                prior += -3
                            self.tile[board.board[y][x][0]] += 1
                    b.append((crossroad, prior))
            b = sorted(b, key=lambda x: x[1], reverse=True)
            if self.list_settlements:
                for tile in self.near_tile(b[0][0], board):
                    self.res[tile[0]] += 1
            self.list_settlements.append(b[0][0])
            self.win_points += 1
        else:
            if a:
                x, y = a[0]
                self.res["Глинянный карьер"] -= 1
                self.res["Лес"] -= 1
                self.res["Пашня"] -= 1
                self.res["Луг"] -= 1
                self.list_settlements.append((x, y))
                self.win_points += 1

    def build_road(self, player_roads, list_crossroad_coord, start=False):
        a = self.when_build_road(player_roads, list_crossroad_coord, start=start)
        if start:
            x0, y0 = self.list_settlements[0]
            x1, y1 = self.list_settlements[-1]
            b = []
            for x, y in a:
                prior = 0
                if x0 < x < x1 or x0 > x > x1:
                    prior += 1
                if y0 < y < y1 or y0 > y > y1:
                    prior += 1
                b.append([(x, y), prior])
            b = sorted(b, key=lambda x: x[1], reverse=True)
            self.roads.append([(x1, y1), b[0][0]])
        else:
            b = set()
            for road in self.roads:
                b.add(road[0])
                b.add(road[1])
            for crossroad in b:
                x, y = crossroad
                a = self.when_build_road(player_roads, list_crossroad_coord, x, y)
                if a:
                    break
            if a:
                self.roads.append([(x, y), a[0]])
                self.res["Глинянный карьер"] -= 1
                self.res["Лес"] -= 1

    def trade(self):
        b = list(self.res.items())
        b.sort(key=lambda x: x[1],reverse=True)
        if b[0][1] > 4:
            self.res[b[0][0]] -= 4
            self.res[b[-1][0]] += 1

    def build_citi(self):
        if self.list_settlements:
            self.list_cities.append(self.list_settlements[0])
            del self.list_settlements[0]
            self.res["Пашня"] -= 2
            self.res["Гора"] -= 3


