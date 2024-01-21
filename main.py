from classes import *
from functions import *


class Game:
    def __init__(self):
        self.turn = 0
        self.board = Board()
        self.player = Player()
        self.bot = GameBot()
        self.starting = True
        self.step = 0

        self.pos = None

    def play(self, pos=None):
        global TEXT, EVENT
        if self.turn == 0:
            if self.step == 0:
                a = random.randint(1, 6)
                a += random.randint(1, 6)
                self.player.get_res(a, self.board)
                self.bot.get_res(a, self.board)
                self.step += 1
                TEXT = "Фаза торговли"
                return
            '''if self.step == 1:
                return'''
            if self.step == 2:
                TEXT = "Фаза строительства"
                if pos or self.pos:
                    if pos:
                        self.pos = pos
                    if EVENT == 1:
                        if self.player.res["Глинянный карьер"] > 0 and self.player.res["Лес"] > 0:
                            if not self.player.build_road(self.bot.roads, self.board.crossroad_coords, self.pos):
                                return
                        EVENT = None
                    if EVENT == 2:
                        if (self.player.res["Глинянный карьер"] > 0 and
                                self.player.res["Лес"] > 0 and
                                self.player.res["Пашня"] > 0 and
                                self.player.res["Луг"] > 0):
                            bot_construction = self.bot.list_settlements + self.bot.list_cities
                            if not self.player.build_settlement(bot_construction, self.board, self.pos):
                                return
                        EVENT = None
                    if EVENT == 3:
                        if self.player.res["Пашня"] > 1 and self.player.res["Гора"] > 2:
                            if not self.player.build_citi(self.pos):
                                return
                        EVENT = None
                self.pos = None
                return
            if self.step == 3:
                self.step = 0
                self.turn = 1
        else:
            a = random.randint(1, 6)
            a += random.randint(1, 6)
            self.player.get_res(a, self.board)
            self.bot.get_res(a, self.board)
            self.bot.trade()
            if (self.bot.res["Глинянный карьер"] > 0 and
                    self.bot.res["Лес"] > 0 and
                    self.bot.res["Пашня"] > 0 and
                    self.bot.res["Луг"] > 0):
                player_construction = self.player.list_settlements + self.player.list_cities
                self.bot.build_settlement(player_construction, self.board)
            if self.bot.res["Пашня"] > 1 and self.bot.res["Гора"] > 2:
                self.bot.build_citi()
            if self.bot.res["Глинянный карьер"] > 0 and self.bot.res["Лес"] > 0:
                if not self.bot.when_build_settlement(self.player.list_settlements + self.player.list_cities,
                                                      self.board.crossroad_coords):
                    self.bot.build_road(self.player.roads, self.board.crossroad_coords)
            self.turn = 0

    def start(self, pos):
        global TEXT
        if self.step == 0:
            if self.player.build_settlement([], self.board, pos, self.starting):
                self.step += 1
                TEXT = " Вы строите дорогу"
                return
        if self.step == 1:
            if self.player.build_road([], self.board.crossroad_coords, pos, self.starting):
                self.step += 1
        self.turn = 1
        for i in range(2):
            if self.step == 2 + i * 2:
                self.bot.build_settlement(self.player.list_settlements, self.board, self.starting)
                self.step += 1
            if self.step == 3 + i * 2:
                self.bot.build_road([], self.board.crossroad_coords, self.starting)
                self.step += 1
        self.turn = 0
        if self.step == 6:
            TEXT = " Вы строите поселение"
            if self.player.build_settlement(self.bot.list_settlements, self.board, pos, self.starting):
                self.step += 1
                TEXT = " Вы строите дорогу"
                return
        if self.step == 7:
            if self.player.build_road(self.bot.roads, self.board.crossroad_coords, pos, self.starting):
                self.step += 1
                self.starting = False
                TEXT = ""
                self.step = 0

    def render(self, screen):
        pr, br = self.player.roads, self.bot.roads
        pc = self.player.list_settlements + self.player.list_cities
        bc = self.bot.list_settlements + self.bot.list_cities
        pi, bi = len(self.player.list_settlements), len(self.bot.list_settlements)
        self.board.render(screen, pr, br, pc, pi, bc, bi)

    def trade(self):
        if not (PRODUCT1 and PRODUCT2):
            return
        if self.player.res[res_tile[PRODUCT1]] > 3:
            self.player.res[res_tile[PRODUCT1]] -= 4
            self.player.res[res_tile[PRODUCT2]] += 1


MYEVENTTYPE = pygame.USEREVENT + 10
music_const = 1
music_list = ["music/1.mp3", "music/2.mp3"]
pygame.time.set_timer(MYEVENTTYPE, 60000)
pygame.display.set_caption("Catan")
clock = pygame.time.Clock()
start_screen(screen)
pygame.mixer.music.load("music/2.mp3")
pygame.mixer.music.play(-1)
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
btn_step = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(size[0] - 170, size[1] - 250, 170, 35),
    text="Следующая фаза",
    manager=manager
)
list_trade = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=["Лес", "Глина", "Камень", "Пшеница", "Овцы"], starting_option="Лес",
    relative_rect=pygame.Rect(size[0] - 100, size[1] - 300, 100, 50),
    manager=manager
)
btn_trade = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(size[0] - 170, size[1] - 350, 170, 50),
    text="Обменять товар",
    manager=manager
)
list_trade1 = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=["Лес", "Глина", "Камень", "Пшеница", "Овцы"], starting_option="Лес",
    relative_rect=pygame.Rect(size[0] - 200, size[1] - 300, 100, 50),
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
            else:
                game.play(pos=event.pos)
        if event.type == MYEVENTTYPE:
            music_const = (music_const + 1) % 2
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_list[music_const])
            pygame.mixer.music.play(-1)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                terminate()
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == list_trade1:
                    PRODUCT1 = event.text
                else:
                    PRODUCT2 = event.text
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if not game.starting:
                    if event.ui_element == btn_road:
                        EVENT = 1
                    elif event.ui_element == btn_settlement:
                        EVENT = 2
                    elif event.ui_element == btn_city:
                        EVENT = 3
                    elif event.ui_element == btn_step:
                        if game.turn == 0:
                            game.step += 1
                    elif event.ui_element == btn_trade:
                        if game.step == 1 and game.turn == 0:
                            game.trade()
        if event.type != MYEVENTTYPE:
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
    show_text(screen, "ПО: " + str(game.player.win_points), (200, size[1] - 50))
    show_text(screen, "ПО: " + str(game.bot.win_points), (10, 100))
    show_text(screen, TITLE, (size[0] * 4 // 9, 30))
    pygame.draw.rect(screen, (0, 0, 255), (size[0] - 370, size[0] - 57, 370, 85))
    # ---------------
    game.render(screen)
    manager.update(time_delta)
    manager.draw_ui(screen)
    clock.tick(FPS)
    pygame.display.flip()
    if game.player.win_points == 10 or game.bot.win_points == 10:
        text = "Вы проиграли!"
        if game.player.win_points == 10:
            text = " Вы выиграли!"
        game.player = Player()
        game.bot = GameBot()
        game.starting = True
        game.step = 0
        TEXT = " Вы строите поселение"
        finish_screen(screen, text)
pygame.quit()