import os
import sys

import pygame_gui

from constants import *

pygame.init()
size = (701, 701)
screen = pygame.display.set_mode(size)


def terminate():
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


def show_text(screen, tex, pos, size=30, color=(0, 0, 0)):
    if tex in "68":
        color = (255, 0, 0)
    font = pygame.font.Font(None, size)
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
    pygame.mixer.music.load("music/Заставка.mp3")
    pygame.mixer.music.play(-1)
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
    clock = pygame.time.Clock()
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
                        pygame.mixer.music.stop()
                        return
                    if event.ui_element == switch_exit:
                        exit(manager)

            manager.process_events(event)
        screen.blit(fon, (0, 0))
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

def finish_screen(screen, text):
    manager = pygame_gui.UIManager((size[0] - 100, size[1] - 100))
    fon = load_image("fon.jpg", size)
    screen.blit(fon, (0, 0))
    btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, size[1] - 160), (150, 50)),
        text=text,
        manager=manager
    )
    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(manager)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    terminate()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn:
                        start_screen(screen)
                        return
            manager.process_events(event)
        screen.blit(fon, (0, 0))
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

