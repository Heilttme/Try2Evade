import pygame
import sys
import os
import random
import sqlite3
import time

FPS = 120


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
    return image


class Main_menu_square(pygame.sprite.Sprite):  #########################################################
    def __init__(self):
        super().__init__(menu_sprites)
        self.image_smile = load_image("square_smile.png", -1)
        self.image_smile = pygame.transform.scale(self.image_smile, (100, 100))
        self.image_smile.convert_alpha()

        self.image = self.image_smile
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = random.randint(3, 8)
        self.vy = random.randint(3, 8)

        self.changed = False

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy

        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Main_Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(main_sprites)
        self.image_smile = load_image("square_smile.png", -1)
        self.image_smile = pygame.transform.scale(self.image_smile, (100, 100))
        self.image_smile.convert_alpha()

        self.status = True
        self.image = self.image_smile
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 50
        self.rect.y = height // 2 - 50
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, lvl):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.status = False
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.status = False
        if pygame.sprite.spritecollideany(self, enemy_sprites_lvl1) and lvl == 0:
            self.status = False
        if pygame.sprite.spritecollideany(self, enemy_sprites_lvl2) and lvl == 1:
            self.status = False
        if pygame.sprite.spritecollideany(self, enemy_sprites_lvl3) and lvl == 2:
            self.status = False
        if pygame.sprite.spritecollideany(self, enemy_sprites_lvl4) and lvl == 3:
            self.status = False


class Enemy_Rectengular(pygame.sprite.Sprite):
    def __init__(self, n, coords, vx, vy, side_size):
        if n == 1:
            super().__init__(enemy_sprites_lvl1)
        elif n == 2:
            super().__init__(enemy_sprites_lvl2)
        elif n == 3:
            super().__init__(enemy_sprites_lvl3)
        elif n == 4:
            super().__init__(enemy_sprites_lvl4)

        self.vx = vx
        self.vy = vy

        self.image_no_smile = load_image("square_nosmile.png", -1)
        self.image_no_smile = pygame.transform.scale(self.image_no_smile, (side_size, side_size))
        self.image_no_smile.convert_alpha()

        self.image = self.image_no_smile
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Enemy_Circle(pygame.sprite.Sprite):
    def __init__(self, n, coords, vx, vy, radius):
        if n == 1:
            super().__init__(enemy_sprites_lvl1)
        elif n == 2:
            super().__init__(enemy_sprites_lvl2)
        elif n == 3:
            super().__init__(enemy_sprites_lvl3)
        elif n == 4:
            super().__init__(enemy_sprites_lvl4)

        self.vx = vx
        self.vy = vy

        self.image_circle = load_image('circle.png', -1)
        self.image_circle = pygame.transform.scale(self.image_circle, (radius * 2, radius * 2))
        self.image_circle.convert_alpha()

        self.image = self.image_circle
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(border_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def terminate():
    running = False
    pygame.quit()
    sys.exit()


def main_game(event_lvl):
    main_hero = Main_Character()
    move = False
    running = True
    start = False
    win = False
    set = False
    time_started = False
    time_left1 = 8
    time_left2 = 7
    time_left3 = 6
    time_left4 = 5
    while running:
        screen.fill((255, 255, 255))
        if event_lvl == 0:
            enemy_sprites_lvl1.draw(screen)
        elif event_lvl == 1:
            enemy_sprites_lvl2.draw(screen)
        elif event_lvl == 2:
            enemy_sprites_lvl3.draw(screen)
        elif event_lvl == 3:
            enemy_sprites_lvl4.draw(screen)
        main_sprites.draw(screen)
        border_sprites.draw(screen)
        if start:
            if main_hero.status:
                if not time_started:
                    start_ticks = pygame.time.get_ticks()
                    time_started = True
                seconds = (pygame.time.get_ticks() - start_ticks) / 1000
                if event_lvl == 0:
                    time = int(time_left1 - seconds)
                elif event_lvl == 1:
                    time = int(time_left2 - seconds)
                elif event_lvl == 2:
                    time = int(time_left3 - seconds)
                elif event_lvl == 3:
                    time = int(time_left4 - seconds)

                time_rendered = fontmid.render(str(time), 1, pygame.Color('black'))
                timer_text_rect = time_rendered.get_rect()
                timer_text_rect.x = 10
                timer_text_rect.y = 10
                screen.blit(time_rendered, timer_text_rect)

                if time <= 0:
                    main_hero.status = False
                    win = True

                if event_lvl == 0:
                    enemy_sprites_lvl1.update()
                elif event_lvl == 1:
                    enemy_sprites_lvl2.update()
                elif event_lvl == 2:
                    enemy_sprites_lvl3.update()
                elif event_lvl == 3:
                    enemy_sprites_lvl4.update()
                main_sprites.update(event_lvl)
                border_sprites.update()

                main_hero_coords = (main_hero.rect.topleft, main_hero.rect.bottomright)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        position = event.pos
                        if main_hero_coords[0][0] <= position[0] and main_hero_coords[1][0] >= position[0] and \
                                main_hero_coords[0][1] <= position[1] and main_hero_coords[1][1] >= position[1]:
                            move = True

                    if event.type == pygame.MOUSEMOTION:
                        if move:
                            main_hero.rect.topleft = (
                                main_hero.rect.topleft[0] + event.rel[0], main_hero.rect.topleft[1] + event.rel[1])

                    if event.type == pygame.MOUSEBUTTONUP:
                        move = False

            if not main_hero.status:
                if not win:
                    lose_text = ['Вы проиграли,', 'попробуйте снова:', 'Начать уровень заново', 'В главное меню',
                                 'Осталось продержаться:']
                    string_rendered1 = fontsmall.render(lose_text[0], 1, pygame.Color('black'))
                    string_rendered2 = fontsmall.render(lose_text[1], 1, pygame.Color('black'))
                    string_rendered3 = fontmid.render(lose_text[2], 1, pygame.Color('black'))
                    string_rendered4 = fontmid.render(lose_text[3], 1, pygame.Color('black'))
                    if event_lvl == 0:
                        string_rendered5 = fontsmall.render(f'{lose_text[4]} {str(int(time_left1 - seconds))} секунд',
                                                            1, pygame.Color('black'))
                    elif event_lvl == 1:
                        string_rendered5 = fontsmall.render(f'{lose_text[4]} {str(int(time_left2 - seconds))} секунд',
                                                            1, pygame.Color('black'))
                    elif event_lvl == 2:
                        string_rendered5 = fontsmall.render(f'{lose_text[4]} {str(int(time_left3 - seconds))} секунд',
                                                            1, pygame.Color('black'))
                    elif event_lvl == 3:
                        string_rendered5 = fontsmall.render(f'{lose_text[4]} {str(int(time_left4 - seconds))} секунд',
                                                            1, pygame.Color('black'))

                    text1 = string_rendered1.get_rect()
                    text2 = string_rendered2.get_rect()
                    text3 = string_rendered3.get_rect()
                    text4 = string_rendered4.get_rect()
                    text5 = string_rendered4.get_rect()

                    text1.x = width - 500
                    text1.y = 50

                    text2.x = width - 500
                    text2.y = 90

                    text3.x = width - 500
                    text3.y = 130

                    text4.x = width - 500
                    text4.y = 180

                    text5.x = width - 500
                    text5.y = 230

                    bg = pygame.draw.rect(screen, (255, 255, 255), (750, 6, 530, 300))
                    screen.blit(string_rendered1, text1)
                    screen.blit(string_rendered2, text2)
                    screen.blit(string_rendered3, text3)
                    screen.blit(string_rendered4, text4)
                    screen.blit(string_rendered5, text5)

                    restart_coords = (text3.topleft, text3.bottomright)
                    main_menu_coords = (text4.topleft, text4.bottomright)
                    main_hero_coords = (main_hero.rect.topleft, main_hero.rect.bottomright)
                    if not set:
                        if event_lvl == 0:
                            current_loses = cur.execute("""SELECT loses from statistics1""").fetchone()[0] + 1
                            current_tries = cur.execute("""SELECT tries from statistics1""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics1 SET tries = '{current_tries}' """)
                            con.commit()
                            cur.execute(f"""UPDATE statistics1 SET loses = '{current_loses}' """)
                            con.commit()

                        elif event_lvl == 1:
                            current_loses = cur.execute("""SELECT loses from statistics2""").fetchone()[0] + 1
                            current_tries = cur.execute("""SELECT tries from statistics2""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics2 SET tries = '{current_tries}' """)
                            con.commit()
                            cur.execute(f"""UPDATE statistics2 SET loses = '{current_loses}' """)
                            con.commit()

                        elif event_lvl == 2:
                            current_loses = cur.execute("""SELECT loses from statistics3""").fetchone()[0] + 1
                            current_tries = cur.execute("""SELECT tries from statistics3""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics3 SET tries = '{current_tries}' """)
                            con.commit()
                            cur.execute(f"""UPDATE statistics3 SET loses = '{current_loses}' """)
                            con.commit()

                        elif event_lvl == 3:
                            current_loses = cur.execute("""SELECT loses from statistics4""").fetchone()[0] + 1
                            current_tries = cur.execute("""SELECT tries from statistics4""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics4 SET tries = '{current_tries}' """)
                            con.commit()
                            cur.execute(f"""UPDATE statistics4 SET loses = '{current_loses}' """)
                            con.commit()
                        set = True

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()

                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            position = event.pos
                            if restart_coords[0][0] <= position[0] and restart_coords[1][0] >= position[0] and \
                                    restart_coords[0][1] <= position[1] and restart_coords[1][1] >= position[1]:
                                start_ticks = pygame.time.get_ticks()
                                if event_lvl == 0:
                                    enemies_lvl1()
                                elif event_lvl == 1:
                                    enemies_lvl2()
                                elif event_lvl == 2:
                                    enemies_lvl3()
                                elif event_lvl == 3:
                                    enemies_lvl4()
                                main_sprites.empty()
                                start = False
                                set = False
                                time_started = False
                                main_hero = Main_Character()
                            elif main_menu_coords[0][0] <= position[0] and main_menu_coords[1][0] >= position[0] and \
                                    main_menu_coords[0][1] <= position[1] and main_menu_coords[1][1] >= position[1]:
                                if event_lvl == 0:
                                    enemies_lvl1()
                                elif event_lvl == 1:
                                    enemies_lvl2()
                                elif event_lvl == 2:
                                    enemies_lvl3()
                                elif event_lvl == 3:
                                    enemies_lvl4()
                                main_sprites.empty()
                                start_screen()
                                set = False
                                time_started = False
                else:
                    win_text = ['Поздравляем', 'Вы победили', 'В главное меню', 'Начать сначала']
                    string_win1 = fontbig.render(win_text[0], 1, pygame.Color('black'))
                    string_win2 = fontbig.render(win_text[1], 1, pygame.Color('black'))
                    string_win3 = fontmid.render(win_text[2], 1, pygame.Color('black'))
                    string_win4 = fontmid.render(win_text[3], 1, pygame.Color('black'))

                    text1 = string_win1.get_rect()
                    text2 = string_win2.get_rect()
                    text3 = string_win3.get_rect()
                    text4 = string_win4.get_rect()

                    text1.x = width // 2 - 150
                    text1.y = 10

                    text2.x = width // 2 - 150
                    text2.y = 70

                    text3.x = width // 2 - 150
                    text3.y = 150

                    text4.x = width // 2 - 150
                    text4.y = 190

                    bg = pygame.draw.rect(screen, (255, 255, 255), (480, 6, 400, 250))
                    screen.blit(string_win1, text1)
                    screen.blit(string_win2, text2)
                    screen.blit(string_win3, text3)
                    screen.blit(string_win4, text4)

                    restart_coords = (text4.topleft, text4.bottomright)
                    main_menu_coords = (text3.topleft, text4.bottomright)
                    if not set:
                        if event_lvl == 0:
                            current_wins = cur.execute("""SELECT wins FROM statistics1""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics1 SET wins = '{current_wins}'""")
                            con.commit()

                            current_tries = cur.execute("""SELECT tries from statistics1""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics1 SET tries = '{current_tries}' """)
                            con.commit()

                        elif event_lvl == 1:
                            current_wins = cur.execute("""SELECT wins FROM statistics2""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics2 SET wins = '{current_wins}'""")
                            con.commit()

                            current_tries = cur.execute("""SELECT tries from statistics2""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics2 SET tries = '{current_tries}' """)
                            con.commit()

                        elif event_lvl == 2:
                            current_wins = cur.execute("""SELECT wins FROM statistics3""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics3 SET wins = '{current_wins}'""")
                            con.commit()

                            current_tries = cur.execute("""SELECT tries from statistics3""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics3 SET tries = '{current_tries}' """)
                            con.commit()

                        elif event_lvl == 3:
                            current_wins = cur.execute("""SELECT wins FROM statistics4""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics4 SET wins = '{current_wins}'""")
                            con.commit()

                            current_tries = cur.execute("""SELECT tries from statistics4""").fetchone()[0] + 1
                            cur.execute(f"""UPDATE statistics4 SET tries = '{current_tries}' """)
                            con.commit()

                        set = True

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            position = event.pos
                            if restart_coords[0][0] <= position[0] and restart_coords[1][0] >= position[0] and \
                                    restart_coords[0][1] <= position[1] and restart_coords[1][1] >= position[1]:
                                start_ticks = pygame.time.get_ticks()
                                if event_lvl == 0:
                                    enemies_lvl1()
                                elif event_lvl == 1:
                                    enemies_lvl2()
                                elif event_lvl == 2:
                                    enemies_lvl3()
                                elif event_lvl == 3:
                                    enemies_lvl4()
                                main_sprites.empty()
                                start = False
                                win = False
                                set = False
                                time_started = False
                                main_hero = Main_Character()
                            elif main_menu_coords[0][0] <= position[0] and main_menu_coords[1][0] >= position[0] and \
                                    main_menu_coords[0][1] <= position[1] and main_menu_coords[1][1] >= position[1]:
                                if event_lvl == 0:
                                    enemies_lvl1()
                                elif event_lvl == 1:
                                    enemies_lvl2()
                                elif event_lvl == 2:
                                    enemies_lvl3()
                                elif event_lvl == 3:
                                    enemies_lvl4()
                                main_sprites.empty()
                                start_screen()
                                set = False
                                time_started = False

        if not start:
            main_hero_coords = (main_hero.rect.topleft, main_hero.rect.bottomright)
            text = ['Зажмите ЛКМ на своём персонаже для начала']
            string_rendered = fontsmall.render(text[0], 1, pygame.Color('black'))
            text_rect = string_rendered.get_rect()
            text_rect.x = width // 2 - 300
            text_rect.y = height - 50
            screen.blit(string_rendered, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    start = True

                    position = event.pos
                    if main_hero_coords[0][0] <= position[0] and main_hero_coords[1][0] >= position[0] and \
                            main_hero_coords[0][1] <= position[1] and main_hero_coords[1][1] >= position[1]:
                        move = True

        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ['Try2Evade', '',
                  'Начать игру',
                  'Правила',
                  'Выйти из игры']

    while True:
        screen.fill((255, 255, 255))
        fontbig = pygame.font.Font(None, 100)
        font = pygame.font.Font(None, 60)
        text_coord = 50
        string_rendered = fontbig.render(intro_text[0], 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 450
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        text_pos = dict()

        for i in range(len(intro_text[1:])):
            string_rendered = font.render(intro_text[i + 1], 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            intro_rect.x = 500
            text_coord += intro_rect.height
            text_pos[intro_text[i + 1]] = (intro_rect.topleft, intro_rect.bottomright)
            screen.blit(string_rendered, intro_rect)

        menu_sprites.draw(screen)
        menu_sprites.update()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = event.pos
                for i in text_pos:
                    if text_pos[i][0][0] <= position[0] and text_pos[i][1][0] >= position[0] and text_pos[i][0][1] <= \
                            position[1] and text_pos[i][1][1] >= position[1]:
                        if i == 'Начать игру':
                            return begin_game()
                        elif i == 'Правила':
                            rules()
                        elif i == 'Выйти из игры':
                            terminate()

        def rules():
            rule_text = ["Правила", "",
                         "Назад",
                         "Правила Try2Evade очень просты:",
                         "Чтобы пройти уровень, вам необходимо уклоняться своим",
                         "персонажем от других фигур определённое время."]

            while True:
                screen.fill((255, 255, 255))

                text_coord = 20
                string_rendered = font.render(rule_text[2], 1, pygame.Color('black'))
                rule_rect = string_rendered.get_rect()
                rule_rect.top = text_coord
                rule_rect.x = 40
                text_coord += rule_rect.height
                screen.blit(string_rendered, rule_rect)

                back_coords = (rule_rect.topleft, rule_rect.bottomright)

                text_coord = 60
                string_rendered = fontbig.render(rule_text[0], 1, pygame.Color('black'))
                rule_rect = string_rendered.get_rect()
                text_coord += 10
                rule_rect.top = text_coord
                rule_rect.x = 450
                text_coord += rule_rect.height
                screen.blit(string_rendered, rule_rect)

                text_pos = dict()

                for i in range(len(rule_text[3:])):
                    string_rendered = font.render(rule_text[i + 3], 1, pygame.Color('black'))
                    rule_rect = string_rendered.get_rect()
                    text_coord += 30
                    rule_rect.top = text_coord
                    rule_rect.x = 50
                    text_coord += rule_rect.height
                    text_pos[rule_text[i + 1]] = (rule_rect.topleft, rule_rect.bottomright)
                    screen.blit(string_rendered, rule_rect)

                menu_sprites.draw(screen)
                menu_sprites.update()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        position = event.pos
                        if back_coords[0][0] <= position[0] and back_coords[1][0] >= position[0] and \
                                back_coords[0][1] <= position[1] and back_coords[1][1] >= position[1]:
                            start_screen()
                clock.tick(FPS)

        def begin_game():
            running = True
            lvls = ['1 уровень', '2 уровень', '3 уровень', '4 уровень', 'Аркада', 'Начать', 'Назад']

            stats_text = ['Поражения:', 'Попытки:', 'Победы:']

            lvl_1_stats = [str(cur.execute("""SELECT wins FROM statistics1""").fetchone()[0]),
                           str(cur.execute("""SELECT loses FROM statistics1""").fetchone()[0]),
                           str(cur.execute("""SELECT tries FROM statistics1""").fetchone()[0])]

            lvl_2_stats = [str(cur.execute("""SELECT wins FROM statistics2""").fetchone()[0]),
                           str(cur.execute("""SELECT loses FROM statistics2""").fetchone()[0]),
                           str(cur.execute("""SELECT tries FROM statistics2""").fetchone()[0])]

            lvl_3_stats = [str(cur.execute("""SELECT wins FROM statistics3""").fetchone()[0]),
                           str(cur.execute("""SELECT loses FROM statistics3""").fetchone()[0]),
                           str(cur.execute("""SELECT tries FROM statistics3""").fetchone()[0])]

            lvl_4_stats = [str(cur.execute("""SELECT wins FROM statistics4""").fetchone()[0]),
                           str(cur.execute("""SELECT loses FROM statistics4""").fetchone()[0]),
                           str(cur.execute("""SELECT tries FROM statistics4""").fetchone()[0])]

            while running:
                screen.fill((255, 255, 255))
                border_sprites.update()
                menu_sprites.update()

                b = 100
                begin_coords = list()

                for i in range(len(lvls) - 2):
                    string_rendered = fontsmall.render(lvls[i], 1, pygame.Color('black'))
                    begin_button = fontsmall.render(lvls[-2], 1, pygame.Color('black'))
                    lvl_rect = string_rendered.get_rect()
                    begin_button_rect = begin_button.get_rect()
                    lvl_rect.top = b + 10
                    lvl_rect.x = 40
                    begin_button_rect.top = b + 50
                    begin_button_rect.x = 55

                    pygame.draw.rect(screen, (0, 0, 0),
                                     pygame.Rect(lvl_rect.topleft[0] - 6, lvl_rect.topleft[1] - 6,
                                                 1200, 100))
                    pygame.draw.rect(screen, (255, 255, 255),
                                     pygame.Rect(lvl_rect.topleft[0], lvl_rect.topleft[1],
                                                 1188, 88))

                    pygame.draw.rect(screen, (0, 0, 0),
                                     pygame.Rect(begin_button_rect.topleft[0] - 6, begin_button_rect.topleft[1] - 6,
                                                 begin_button_rect.bottomright[0] - begin_button_rect.topleft[0] + 8,
                                                 begin_button_rect.bottomright[1] - begin_button_rect.topleft[1] + 6))
                    pygame.draw.rect(screen, (255, 255, 255),
                                     pygame.Rect(begin_button_rect.topleft[0] - 4, begin_button_rect.topleft[1] - 4,
                                                 begin_button_rect.bottomright[0] - begin_button_rect.topleft[0] + 4,
                                                 begin_button_rect.bottomright[1] - begin_button_rect.topleft[1] + 2))

                    screen.blit(begin_button, begin_button_rect)
                    screen.blit(string_rendered, lvl_rect)
                    b += 100

                    loses_text = fontsmall.render(str(stats_text[0]), 1, pygame.Color('black'))
                    wins_text = fontsmall.render(str(stats_text[2]), 1, pygame.Color('black'))
                    tries_text = fontsmall.render(str(stats_text[1]), 1, pygame.Color('black'))

                    loses_text_rect = loses_text.get_rect()
                    wins_text_rect = wins_text.get_rect()
                    tries_text_rect = tries_text.get_rect()

                    ## 1 уровень
                    loses_text_rect.x = 250
                    loses_text_rect.y = 135

                    wins_text_rect.x = 500
                    wins_text_rect.y = 135

                    tries_text_rect.x = 750
                    tries_text_rect.y = 135

                    screen.blit(loses_text, loses_text_rect)
                    screen.blit(wins_text, wins_text_rect)
                    screen.blit(tries_text, tries_text_rect)
                    ##
                    ## 2 уровень
                    loses_text_rect.x = 250
                    loses_text_rect.y = 240

                    wins_text_rect.x = 500
                    wins_text_rect.y = 240

                    tries_text_rect.x = 750
                    tries_text_rect.y = 240

                    screen.blit(loses_text, loses_text_rect)
                    screen.blit(wins_text, wins_text_rect)
                    screen.blit(tries_text, tries_text_rect)
                    ##
                    ## 3 уровень
                    loses_text_rect.x = 250
                    loses_text_rect.y = 345

                    wins_text_rect.x = 500
                    wins_text_rect.y = 345

                    tries_text_rect.x = 750
                    tries_text_rect.y = 345

                    screen.blit(loses_text, loses_text_rect)
                    screen.blit(wins_text, wins_text_rect)
                    screen.blit(tries_text, tries_text_rect)
                    ##
                    ## 4 уровень
                    loses_text_rect.x = 250
                    loses_text_rect.y = 440

                    wins_text_rect.x = 500
                    wins_text_rect.y = 440

                    tries_text_rect.x = 750
                    tries_text_rect.y = 440

                    screen.blit(loses_text, loses_text_rect)
                    screen.blit(wins_text, wins_text_rect)
                    screen.blit(tries_text, tries_text_rect)
                    ##
                    ## Аркада
                    loses_text_rect.x = 250
                    loses_text_rect.y = 540

                    wins_text_rect.x = 500
                    wins_text_rect.y = 540

                    tries_text_rect.x = 750
                    tries_text_rect.y = 540

                    screen.blit(loses_text, loses_text_rect)
                    screen.blit(wins_text, wins_text_rect)
                    screen.blit(tries_text, tries_text_rect)
                    ##

                    ## 1 Уровень статистика
                    string_rendered = fontsmall.render(str(lvl_1_stats[1]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 420
                    win_los_try_text.y = 135

                    screen.blit(string_rendered, win_los_try_text)


                    string_rendered = fontsmall.render(str(lvl_1_stats[0]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 625
                    win_los_try_text.y = 135

                    screen.blit(string_rendered, win_los_try_text)


                    string_rendered = fontsmall.render(str(lvl_1_stats[2]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 880
                    win_los_try_text.y = 135

                    screen.blit(string_rendered, win_los_try_text)
                    ##

                    ## 2 Уровень статистика
                    string_rendered = fontsmall.render(str(lvl_2_stats[1]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 420
                    win_los_try_text.y = 240

                    screen.blit(string_rendered, win_los_try_text)

                    string_rendered = fontsmall.render(str(lvl_2_stats[0]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 625
                    win_los_try_text.y = 240

                    screen.blit(string_rendered, win_los_try_text)

                    string_rendered = fontsmall.render(str(lvl_2_stats[2]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 880
                    win_los_try_text.y = 240

                    screen.blit(string_rendered, win_los_try_text)
                    ##

                    ## 3 Уровень статистика
                    string_rendered = fontsmall.render(str(lvl_3_stats[1]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 420
                    win_los_try_text.y = 345

                    screen.blit(string_rendered, win_los_try_text)

                    string_rendered = fontsmall.render(str(lvl_3_stats[0]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 625
                    win_los_try_text.y = 345

                    screen.blit(string_rendered, win_los_try_text)

                    string_rendered = fontsmall.render(str(lvl_3_stats[2]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 880
                    win_los_try_text.y = 345

                    screen.blit(string_rendered, win_los_try_text)
                    ##

                    ## 4 Уровень статистика
                    string_rendered = fontsmall.render(str(lvl_4_stats[1]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 420
                    win_los_try_text.y = 440

                    screen.blit(string_rendered, win_los_try_text)

                    string_rendered = fontsmall.render(str(lvl_4_stats[0]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 625
                    win_los_try_text.y = 440

                    screen.blit(string_rendered, win_los_try_text)

                    string_rendered = fontsmall.render(str(lvl_4_stats[2]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 880
                    win_los_try_text.y = 440

                    screen.blit(string_rendered, win_los_try_text)
                    ##

                    ## Аркада статистика
                    string_rendered = fontsmall.render(str(lvl_1_stats[1]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 420
                    win_los_try_text.y = 135

                    screen.blit(string_rendered, win_los_try_text)

                    string_rendered = fontsmall.render(str(lvl_1_stats[0]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 625
                    win_los_try_text.y = 135

                    screen.blit(string_rendered, win_los_try_text)

                    string_rendered = fontsmall.render(str(lvl_1_stats[2]), 1, pygame.Color('black'))
                    win_los_try_text = string_rendered.get_rect()

                    win_los_try_text.x = 880
                    win_los_try_text.y = 135

                    screen.blit(string_rendered, win_los_try_text)
                    ##



                    begin_coords.append((begin_button_rect.topleft, begin_button_rect.bottomright))

                string_rendered = font.render(lvls[-1], 1, pygame.Color('black'))
                lvl_rect = string_rendered.get_rect()
                lvl_rect.top = 35
                lvl_rect.x = 40
                screen.blit(string_rendered, lvl_rect)
                back_coords = (lvl_rect.topleft, lvl_rect.bottomright)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        position = event.pos
                        if back_coords[0][0] <= position[0] and back_coords[1][0] >= position[0] and \
                                back_coords[0][1] <= position[1] and back_coords[1][1] >= position[1]:
                            start_screen()
                        for i in range(len(begin_coords)):
                            if begin_coords[i][0][0] <= position[0] and begin_coords[i][1][0] >= position[0] and \
                                    begin_coords[i][0][1] <= position[1] and begin_coords[i][1][1] >= position[1]:
                                event_lvl = i
                                main_game(event_lvl)
                                return
                    elif event.type == pygame.MOUSEMOTION:
                        pass
                pygame.display.flip()

        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1280, 720
    pygame.display.set_caption('Try2Evade')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    con = sqlite3.connect('stats.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS statistics1 (
            loses INTEGER,
            wins INTEGER,
            tries INTEGER)""")
    con.commit()
    res = cur.execute("""SELECT count(*) FROM statistics1""").fetchone()[0]
    if res == 0:
        cur.execute(f"""INSERT INTO statistics1 VALUES (?, ?, ?)""",
                    (0, 0, 0))

    cur.execute("""CREATE TABLE IF NOT EXISTS statistics2 (
                loses INTEGER,
                wins INTEGER,
                tries INTEGER)""")
    con.commit()
    res = cur.execute("""SELECT count(*) FROM statistics2""").fetchone()[0]
    if res == 0:
        cur.execute(f"""INSERT INTO statistics2 VALUES (?, ?, ?)""",
                    (0, 0, 0))

    cur.execute("""CREATE TABLE IF NOT EXISTS statistics3 (
                loses INTEGER,
                wins INTEGER,
                tries INTEGER)""")
    con.commit()
    res = cur.execute("""SELECT count(*) FROM statistics3""").fetchone()[0]
    if res == 0:
        cur.execute(f"""INSERT INTO statistics3 VALUES (?, ?, ?)""",
                    (0, 0, 0))

    cur.execute("""CREATE TABLE IF NOT EXISTS statistics4 (
                loses INTEGER,
                wins INTEGER,
                tries INTEGER)""")
    con.commit()
    res = cur.execute("""SELECT count(*) FROM statistics4""").fetchone()[0]
    if res == 0:
        cur.execute(f"""INSERT INTO statistics4 VALUES (?, ?, ?)""",
                    (0, 0, 0))
    con.commit()

    fontsmall = pygame.font.Font(None, 40)
    fontmid = pygame.font.Font(None, 60)
    fontbig = pygame.font.Font(None, 80)

    border_sprites = pygame.sprite.Group()
    menu_sprites = pygame.sprite.Group()
    main_sprites = pygame.sprite.Group()
    enemy_sprites_lvl1 = pygame.sprite.Group()
    enemy_sprites_lvl2 = pygame.sprite.Group()
    enemy_sprites_lvl3 = pygame.sprite.Group()
    enemy_sprites_lvl4 = pygame.sprite.Group()


    def enemies_lvl1():
        enemy_sprites_lvl1.empty()
        en1_1 = Enemy_Rectengular(1, (200, 300), 10, 10, 100)
        en1_2 = Enemy_Rectengular(1, (800, 400), -8, 8, 200)
        en1_3 = Enemy_Circle(1, (400, 400), -5, -10, 50)


    def enemies_lvl2():
        enemy_sprites_lvl2.empty()
        en2_1 = Enemy_Rectengular(2, (800, 300), -8, 12, 50)
        en2_2 = Enemy_Rectengular(2, (100, 400), 8, -8, 150)
        en2_3 = Enemy_Circle(2, (900, 200), 8, 10, 50)


    def enemies_lvl3():
        enemy_sprites_lvl3.empty()
        en3_1 = Enemy_Rectengular(3, (200, 300), 10, 10, 100)
        en3_2 = Enemy_Rectengular(3, (900, 200), -8, 8, 200)
        en3_3 = Enemy_Circle(3, (200, 400), 5, -10, 50)
        en3_4 = Enemy_Circle(3, (800, 400), -5, 10, 50)


    def enemies_lvl4():
        enemy_sprites_lvl4.empty()
        en4_1 = Enemy_Rectengular(4, (200, 300), 10, 10, 200)
        en4_2 = Enemy_Rectengular(4, (800, 400), -8, 8, 200)
        en4_3 = Enemy_Circle(4, (400, 400), -10, -15, 30)


    enemies_lvl1()
    enemies_lvl2()
    enemies_lvl3()
    enemies_lvl4()

    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)

    Main_menu_square()
    Main_menu_square()
    Main_menu_square()
    start_screen()
