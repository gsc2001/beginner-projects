import pygame
import sys
import random
import math
from configparser import RawConfigParser

# ------------------------------GLOBALS---------------------------------------------------------------
pygame.init()
rcp = RawConfigParser()
rcp.read('config.ini')
windowx, windowy = (int(k.strip()) for k in
                    (rcp.get('GENERAL', 'window_size')[1:-1].split(',')))
caption = rcp.get('GENERAL', 'name')
scorebar_width = 50
screenx, screeny = windowx, windowy - scorebar_width
win = pygame.display.set_mode((windowx, windowy))
background_image = pygame.image.load('player_assets/background.jpg')
background_image = pygame.transform.scale(background_image, (windowx, windowy))
pygame.display.set_caption(caption)
FPS = rcp.getint('GENERAL', 'FPS')
fpsclock = pygame.time.Clock()
divisions = 5
width_safe = screeny / (3 * divisions + 1)
width_division = 3 * width_safe
width_water = width_division - width_safe
obstacles_positions = list()
obstacles = pygame.sprite.Group()
safe_areas = pygame.sprite.Group()
MAX_OBSTACLES_IN_ANY_LEVEL = 15
MAX_MIN_OBSTACLES_IN_ANY_LEVEL = 4
MAX_OBSTACLES = 2
MIN_OBSTACLES = 0
font_name = rcp.get('FONT', 'font')
small_font = pygame.font.Font(font_name, scorebar_width // 2)
big_font = pygame.font.Font(font_name, windowy // 10)
medium_font = pygame.font.Font(font_name, windowy // 20)
big_font_color = eval(rcp.get('COLOR', 'big_font_color'))
medium_font_color = eval(rcp.get('COLOR', 'medium_font_color'))
small_font_color = eval(rcp.get('COLOR', 'small_font_color'))
level = 0
seconds = 0
counter = 0
score_decrease_mov_obstacle = 5
score_decrease_stat_obstacle = 10
moving_obstacle_score_increase = 10
stat_obstacle_score_increase = 5
mov_obstacles_speed = [screenx / 300, screenx / 300]
speed_increase_factor = 1.4
timer = 30
player_speed = (windowx / 250, windowy / 250)
player_speed_running = (windowx / 100, windowy / 100)
safe_area_color = eval(rcp.get('COLOR', 'safe_area_color'))
pygame.mixer.music.load('player_assets/background.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
ouch_sound = pygame.mixer.Sound('player_assets/ouch.wav')
message_player1_win = rcp.get('MESSAGE', 'message_player1_win')
message_player2_win = rcp.get('MESSAGE', 'message_player2_win')
message_both_win = rcp.get('MESSAGE', 'message_both_win')
message_nobody_win = rcp.get('MESSAGE', 'message_nobody_win')
crash_message = rcp.get('MESSAGE', 'crash_message')
successful_message = rcp.get('MESSAGE', 'successful_message')
world_end_message = rcp.get('MESSAGE', 'world_end_message')
time_over_message = rcp.get('MESSAGE', 'time_over_message')
winning_message = rcp.get('MESSAGE', 'winning_message')


# ------------------------------------------CLASSES------------------------------------------

class Item(pygame.sprite.Sprite):
    def __init__(self, initx, inity, sizex, sizey):
        super().__init__()
        self.surface = pygame.Surface((sizex, sizey))
        self.rect = self.surface.get_rect()
        self.rect.center = (initx, inity)
        self.sizex = sizex
        self.sizey = sizey
        self.initx = initx
        self.inity = inity

    def show(self, window):
        window.blit(self.surface, (self.rect.x, self.rect.y))


class MovingItem(Item):
    def __init__(self, initx, inity, sizex, sizey, speedx, speedy, typ):
        Item.__init__(self, initx, inity, sizex, sizey)
        self.speedx = speedx
        self.speedy = speedy
        self.typ = typ

    def move(self, direc):
        if direc == 'up':
            self.rect.y = (self.rect.y - self.speedy) % screeny
        if direc == 'right':
            self.rect.x = self.rect.x + self.speedx
            if self.rect.x >= screenx - self.sizex:
                self.typ = 'left'
                self.surface = pygame.transform.flip(self.surface, True, False)
        if direc == 'left':
            self.rect.x = self.rect.x - self.speedx
            if self.rect.x <= 0:
                self.typ = 'right'
                self.surface = pygame.transform.flip(self.surface, True, False)
        if direc == 'down':
            self.rect.y = (self.rect.y + self.speedy) % screeny

    def is_collided_with(self, item):
        return self.rect.colliderect(item.rect)


class Player(MovingItem):

    def __init__(self, initx, inity, sizex, sizey, speedx, speedy, typ):
        MovingItem.__init__(self, initx, inity, sizex, sizey, speedx, speedy,
                            typ)
        self.score = 60
        self.passed = pygame.sprite.Group()
        self.land_surface = pygame.image.load(
            'player_assets/player_final_f.png')
        self.water_surface = pygame.image.load('player_assets/player+boat.png')
        if typ == 'player2':
            self.water_surface = pygame.transform.flip(self.water_surface,
                                                       False, True)
            self.land_surface = pygame.transform.flip(self.land_surface,
                                                      False, True)
        self.surface = self.land_surface.copy()
        self.rect = self.surface.get_rect()
        self.rect.center = (initx, inity)
        self.swimming = False
        self.passed_y = []
        self.level_done = False
        self.running = False

    def swim(self):
        temp_rect = self.rect
        self.surface = self.water_surface.copy()
        self.rect = self.surface.get_rect()
        self.rect.center = temp_rect.center
        self.sizex = self.rect.width
        self.sizey = self.rect.height

    def walk(self):
        temp_rect = self.rect
        self.surface = self.land_surface.copy()
        self.rect = self.surface.get_rect()
        self.rect.center = temp_rect.center
        self.sizex = self.rect.width
        self.sizey = self.rect.height
        del temp_rect

    def move(self, direc):
        if direc == 'up':
            self.rect.y = max([self.rect.y - self.speedy, scorebar_width])
        if direc == 'right':
            self.rect.x = min([self.rect.x + self.speedx,
                               screenx - self.surface.get_width()])
        if direc == 'left':
            self.rect.x = max([self.rect.x - self.speedx, 0])
        if direc == 'down':
            self.rect.y = min([self.rect.y + self.speedy,
                               scorebar_width + screeny - self.sizey])

    def decrease_score(self, obs):

        if isinstance(obs, MovingItem):
            self.score -= score_decrease_mov_obstacle
        else:
            self.score -= score_decrease_stat_obstacle

    def detect_pass_and_increase_score(self):
        for obstacle in obstacles:
            if obstacle not in self.passed:
                if self.typ == 'player1':
                    if obstacle.rect.top >= self.rect.bottom:
                        self.passed.add(obstacle)
                        if isinstance(obstacle, MovingItem):
                            self.score += moving_obstacle_score_increase
                        else:
                            if obstacle.rect.top not in self.passed_y:
                                self.passed_y.append(obstacle.rect.y)
                                self.score += stat_obstacle_score_increase
                else:
                    if obstacle.rect.bottom <= self.rect.top:
                        self.passed.add(obstacle)
                        if isinstance(obstacle, MovingItem):
                            self.score += moving_obstacle_score_increase
                        else:
                            if obstacle.rect.top not in self.passed_y:
                                self.passed_y.append(obstacle.rect.y)
                                self.score += stat_obstacle_score_increase

    def start_running(self):
        self.running = True
        self.speedx, self.speedy = player_speed_running

    def stop_running(self):
        self.running = False
        self.speedx, self.speedy = player_speed


cover_screen = Item(windowx / 2, windowy / 2, windowx, windowy)
cover_screen.surface = cover_screen.surface.convert_alpha()


# ---------------------------- FUNCTIONS--------------------------------------

def generate_obstacles():
    obstacles_positions.clear()
    for div in range(1, divisions):
        no_of_obstacles = random.randint(MIN_OBSTACLES, MAX_OBSTACLES)
        obstacles_positions.append([])
        for _ in range(0, no_of_obstacles):
            posx = random.random() * screenx + width_safe / 2
            posy = scorebar_width + div * width_division + width_safe / 2
            obstacles_positions[-1].append((posx, posy))
    obstacles.__init__()
    for div in range(0, divisions - 1):
        no = len(obstacles_positions[div])
        for _ in range(0, no):
            posx, posy = obstacles_positions[div][_]
            obst = Item(posx, posy, width_safe, width_safe)
            if not pygame.sprite.spritecollideany(obst, obstacles):
                obstacles.add(obst)

    generate_moving_obstacles()


def draw_obstacles():
    for obs in obstacles:
        obs.show(win)


def generate_background():
    y = scorebar_width
    for _ in range(0, divisions + 1):
        safe_area = Item(win.get_width() / 2, y + width_safe / 2,
                         win.get_width(), width_safe)
        safe_areas.add(safe_area)
        safe_area.surface.fill(safe_area_color)
        y += width_division


def draw_background():
    win.blit(background_image, (0, 0))
    for safe_area in safe_areas:
        safe_area.show(win)
    if player_index == 0:
        text, text_rect = text_object("START",
                                      (windowx / 2, windowy - width_safe / 2),
                                      small_font, (0, 0, 0))
        win.blit(text, text_rect)
        del text, text_rect
        text, text_rect = text_object("END",
                                      (windowx / 2,
                                       scorebar_width + width_safe / 2),
                                      small_font, (0, 0, 0))
        win.blit(text, text_rect)
        del text, text_rect
    else:
        text, text_rect = text_object("END",
                                      (windowx / 2, windowy - width_safe / 2),
                                      small_font, (0, 0, 0))
        win.blit(text, text_rect)
        del text, text_rect
        text, text_rect = text_object("START", (
            windowx / 2, scorebar_width + width_safe / 2), small_font,
                                      (0, 0, 0))
        win.blit(text, text_rect)
        del text, text_rect
    draw_obstacles()


def change_player(player_i, player_array):
    current = player_array[player_i]
    current.stop_running()
    current.rect.center = (current.initx, current.inity)
    player_i ^= 1
    return player_i, player_array[player_i]


def render_multi_line(surface, text, x, y, fsize, font, color):
    lines = text.splitlines()
    for i_, l in enumerate(lines):
        surface.blit(font.render(l, 0, color), (x, y + fsize * i_))


def generate_moving_obstacles():
    y = width_safe + scorebar_width
    for div in range(0, divisions):
        if random.randint(0, 1):
            y += width_water / 4

            moving_obstacle = MovingItem(random.random() * screenx, y,
                                         width_water / 3, width_water / 3,
                                         screenx / 200,
                                         0, ['right', 'left'][
                                             random.randint(0, 1)])
            obstacles.add(moving_obstacle)
            y += width_water / 2
            moving_obstacle = MovingItem(random.random() * screenx, y,
                                         width_water / 3, width_water / 3,
                                         screenx / 200, 0, ['right', 'left'][
                                             random.randint(0, 1)])
            obstacles.add(moving_obstacle)
            y += width_water / 4
            y += width_safe
        else:
            y += width_water / 2
            moving_obstacle = MovingItem(random.random() * screenx, y,
                                         width_water / 1.5, width_water / 1.5,
                                         screenx / 200, 0,
                                         ['right1', 'right1'][
                                             random.randint(0, 1)])
            obstacles.add(moving_obstacle)
            y += width_water / 2
            y += width_safe


def mov_obstacles(mov_speed):
    for obstacle in obstacles:
        if isinstance(obstacle, MovingItem):
            obstacle.speedx = mov_speed[player_index]
            if obstacle.typ in ('right', 'right1'):
                obstacle.move('right')
            else:
                obstacle.move('left')


def set_scores():
    score1 = small_font.render("P1 : " + str(player1.score), True,
                               (255, 255, 255))
    score2 = small_font.render("P2 : " + str(player2.score), True,
                               (255, 255, 255))
    score1_rect = score1.get_rect()
    score2_rect = score2.get_rect()
    score1_rect.x, score1_rect.y = screenx / 20, scorebar_width / 5
    score2_rect.x, score2_rect.y = screenx / 1.3, scorebar_width / 5
    win.blit(score1, score1_rect)
    win.blit(score2, score2_rect)
    del score1, score1_rect, score2, score2_rect


def set_current_player_level():
    current_player_name = small_font.render(
        ['P1', 'P2'][player_index] + "   Speed: %.2f" % (
            mov_obstacles_speed[player_index]) + "      Timer:  " + str(
            timer - seconds), True, small_font_color)
    current_player_rect = current_player_name.get_rect()
    current_player_rect.x = screenx / 5
    current_player_rect.y = scorebar_width / 5
    win.blit(current_player_name, current_player_rect)
    del current_player_rect, current_player_name


def show_scorebar():
    score_bar.show(win)
    set_scores()
    set_current_player_level()


def text_object(message, pos, font, color):
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = pos
    return text, text_rect


def change_level():
    global level, MAX_OBSTACLES, MIN_OBSTACLES, mov_obstacles_speed
    if player1.level_done:
        if player2.level_done:
            if player1.score == player2.score:
                mov_obstacles_speed[0] *= speed_increase_factor
                mov_obstacles_speed[1] *= speed_increase_factor
            elif player1.score > player2.score:
                mov_obstacles_speed[0] *= speed_increase_factor
            else:
                mov_obstacles_speed[1] *= speed_increase_factor
        else:
            mov_obstacles_speed[0] *= speed_increase_factor
    else:
        if player2.level_done:
            mov_obstacles_speed[1] *= speed_increase_factor

    del player1.passed, player1.passed_y, player2.passed, player2.passed_y
    player1.passed = pygame.sprite.Group()
    player2.passed = pygame.sprite.Group()
    player1.passed_y = []
    player2.passed_y = []
    level += 1
    if level % 2 == 0:
        MAX_OBSTACLES = min(MAX_OBSTACLES + 1, MAX_OBSTACLES_IN_ANY_LEVEL)
    else:
        MIN_OBSTACLES = min(MIN_OBSTACLES + 1, MAX_MIN_OBSTACLES_IN_ANY_LEVEL)
    generate_obstacles()
    load_obstacles_images()


def paused():
    pause_text, pause_rect = text_object("PAUSED", (windowx / 2, windowy / 2),
                                         big_font, big_font_color)
    cover_screen.surface.fill((0, 0, 0, 100))
    cover_screen.surface.blit(pause_text, pause_rect)
    cover_screen.show(win)
    del pause_rect, pause_text


def level_change_screen():
    if level == 1:
        cover_screen.surface.blit(background_image, (0, 0))
        message = "RIVER CROSSING \n         GAME"
        render_multi_line(cover_screen.surface, message, windowx / 5,
                          windowy / 8, windowy // 10, big_font, big_font_color)
        last_line = " ".join(list("( Press space to play )"))
        text1 = small_font.render(last_line, True, (255, 255, 255))
        textrect = text1.get_rect()
        textrect.center = (windowx / 2, windowy - windowy / 5)
        cover_screen.surface.blit(text1, textrect)
        cover_screen.show(win)
    else:
        cover_screen.surface.fill((0, 128, 255, 255))
        message_line1 = "WORLD {} Results".format(level - 1)
        text1 = big_font.render(message_line1, True, (255, 255, 255))
        textrect = text1.get_rect()
        textrect.center = (windowx / 2, windowy / 5)
        cover_screen.surface.blit(text1, textrect)
        if player1.level_done:
            if player2.level_done:
                if player1.score == player2.score:
                    message1 = message_both_win
                elif player1.score > player2.score:
                    message1 = message_player1_win
                else:
                    message1 = message_player2_win
            else:
                message1 = message_player1_win
        else:
            if player2.level_done:
                message1 = message_player2_win
            else:
                message1 = message_nobody_win
        message1 = '{0:2s}'.format(' ') + message1
        message = message1 + '\n\nPlayer1 score: {} \nPlayer2 score:' \
                             ' {}\n\n'.format(player1.score, player2.score)
        render_multi_line(cover_screen.surface, message, windowx / 3,
                          windowy / 3, windowy / 15, medium_font,
                          medium_font_color)
        last_line = " ".join(list("( Press space for next world )"))
        text1 = small_font.render(last_line, True, (255, 255, 255))
        textrect = text1.get_rect()
        textrect.center = (windowx / 2, windowy - windowy / 5)
        cover_screen.surface.blit(text1, textrect)
        cover_screen.show(win)
        show_scorebar()


def player_change_screen(flag):
    if player_index != 1:
        message = ""
        for i_ in range(3 * FPS, 0, -1):
            detect_quit()
            if flag == 2:
                message = time_over_message
            elif flag == 1:
                message = crash_message
            elif flag == 0:
                message = winning_message
            text, text_rect = text_object(message, (windowx / 2, windowy / 3),
                                          big_font, big_font_color)
            win.blit(temp_display, temp_display.get_rect())
            cover_screen.surface.fill((0, 0, 0, 200))
            cover_screen.surface.blit(text, text_rect)
            line2 = "Player {} turn".format(2 - player_index)
            text, text_rect = text_object(line2, (windowx / 2, windowy / 1.5),
                                          medium_font, medium_font_color)
            cover_screen.surface.blit(text, text_rect)
            del text, text_rect
            display_counter(math.ceil(i_ / FPS))
            cover_screen.show(win)
            pygame.display.update()
            fpsclock.tick(FPS)
    else:
        detect_quit()
        message = ""
        if flag == 2:
            message = time_over_message
        elif flag == 1:
            message = crash_message
        elif flag == 0:
            message = winning_message
        text, text_rect = text_object(message, (windowx / 2, windowy / 2),
                                      big_font, big_font_color)
        cover_screen.surface.fill((0, 0, 0, 200))
        cover_screen.surface.blit(text, text_rect)
        del text, text_rect
        line2 = world_end_message
        text, text_rect = text_object(line2, (windowx / 2, windowy / 1.5),
                                      medium_font, medium_font_color)
        cover_screen.surface.blit(text, text_rect)
        del text, text_rect
        cover_screen.show(win)
        pygame.display.update()
        pygame.time.delay(1000)


def detect_quit():
    for event_ in pygame.event.get():
        if event_.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event_.type == pygame.KEYDOWN:
            if event_.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def display_counter(time):
    text = "Starting in -:"
    text, text_rect = text_object(text, (windowx / 2, windowy / 1.3),
                                  small_font, small_font_color)
    cover_screen.surface.blit(text, text_rect)
    text2 = str(time)
    text2, text2_rect = text_object(text2, (windowx / 2, windowy / 1.2),
                                    medium_font, medium_font_color)
    cover_screen.surface.blit(text2, text2_rect)
    del text, text_rect, text2, text2_rect


def world_welcome_screen(count):
    for cnt in range(count * FPS, 0, -1):
        detect_quit()
        win.blit(temp_display, temp_display.get_rect())
        cover_screen.surface.fill((0, 0, 0, 200))
        title = "WORLD {}".format(level)
        text1 = big_font.render(title, True, (255, 255, 255))
        textrect = text1.get_rect()
        textrect.center = (windowx / 2, windowy / 5)
        cover_screen.surface.blit(text1, textrect)
        line2 = "Player 1 turn"
        text, text_rect = text_object(line2, (windowx / 2, windowy / 1.5),
                                      medium_font, medium_font_color)
        cover_screen.surface.blit(text, text_rect)
        del text_rect, text
        display_counter(math.ceil(cnt / FPS))
        show_scorebar()
        cover_screen.show(win)
        pygame.display.update()
        fpsclock.tick(FPS)


def change_player_game(flag):
    global temp_display, player_index, player, level_change, seconds
    seconds = 0
    temp_display = win.copy()
    if flag == 0:
        player.level_done = True
    player_change_screen(flag)
    if player_index == 1:
        change_level()
        level_change = True
    player_index, player = change_player(player_index, players)


def isonsafe(current_player):
    for safe in safe_areas:
        if safe.rect.bottom >= current_player.rect.centery >= safe.rect.top:
            return True
    return False


def load_obstacles_images():
    for obs in obstacles:
        if isinstance(obs, MovingItem):
            temp_rect = obs.rect
            if obs.typ[-1] != '1':
                obs.surface = pygame.image.load(
                    'player_assets/boat{}.png'.format(random.randint(1, 2)))
            else:
                obs.surface = pygame.image.load('player_assets/big_boat.png')
            obs.rect = obs.surface.get_rect()
            obs.rect.center = temp_rect.center
            obs.sizex = obs.rect.width
            obs.sizey = obs.rect.height
            if obs.typ in ('right', 'right1'):
                obs.surface = pygame.transform.flip(obs.surface, 1, 0)
        else:
            temp_rect = obs.rect
            obs.surface = pygame.image.load('player_assets/crab.png')

            obs.rect = obs.surface.get_rect()
            obs.rect.center = temp_rect.center
            obs.sizex = obs.rect.width
            obs.sizey = obs.rect.height
            obs.surface = pygame.transform.flip(obs.surface, 0,
                                                random.randint(0, 1))


# -------------------INITIALIZING CALLS-----------------------------------


player1 = Player(screenx / 2, scorebar_width + screeny - width_safe / 2,
                 width_safe, width_safe, player_speed[0], player_speed[1],
                 'player1')
player2 = Player(screenx / 2, scorebar_width + width_safe / 2, width_safe,
                 width_safe, player_speed[0], player_speed[1], 'player2')
player2.surface = pygame.transform.flip(player2.surface, False, True)
players = [player1, player2]
player_index = 0
player = players[player_index]
generate_obstacles()
generate_moving_obstacles()
score_bar = Item(windowx / 2, scorebar_width / 2, screenx, scorebar_width)
score_bar.surface.fill((101, 67, 33))
change_level()
level_change, pause, fullscreen = True, False, False
generate_background()
load_obstacles_images()
draw_background()
temp_display = win.copy()

# ---------------------GAME LOOP--------------------------------------

while True:
    draw_background()
    player.show(win)
    show_scorebar()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not level_change:
                    if pause:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    pause = not pause
                else:
                    level_change = not level_change
                    player1.level_done = False
                    player2.level_done = False
                    player1.score = 60
                    player2.score = 60
                    draw_background()
                    pygame.display.update()
                    temp_display = win.copy()
                    world_welcome_screen(3)
            if event.key == pygame.K_r:
                player.start_running()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                player.stop_running()
    if isonsafe(player):
        player.walk()
    else:
        player.swim()
    if not pause and not level_change:
        counter += 1
        if counter == 60:
            counter = 0
            seconds += 1
            player.score -= 1
        if seconds == timer:
            seconds = 0
            change_player_game(2)
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            player.move('right')
        if pressed[pygame.K_LEFT]:
            player.move('left')
        if pressed[pygame.K_DOWN]:
            player.move('down')
        if pressed[pygame.K_UP]:
            player.move('up')
        obstacle_hit = pygame.sprite.spritecollideany(player, obstacles)
        if obstacle_hit:
            pygame.display.update()
            pygame.mixer.music.pause()
            ouch_sound.play(0)
            for i in range(0, FPS):
                detect_quit()
                fpsclock.tick(FPS)
            pygame.mixer.music.unpause()
            player.decrease_score(obstacle_hit)
            change_player_game(1)
        if player_index == 0:
            if player.rect.y == scorebar_width:
                change_player_game(0)
        else:
            if player.rect.y == windowy - player.surface.get_height():
                change_player_game(0)
        mov_obstacles(mov_obstacles_speed)
        player.detect_pass_and_increase_score()
    elif pause:
        paused()
    elif level_change:
        level_change_screen()
    pygame.display.update()
    fpsclock.tick(FPS)

# created by Gurkirat Singh (2019101069)

