import pygame
from pygame.locals import *
import time
from random import randint
from multiprocessing import Process

class Bullet():
    def __init__(self, direction: str, position):
        self.width, self.height = 30, 30
        self.direction = direction
        self.is_dead = False
        self.bullet_speed = 50
        self.current_x_position = position[0]
        self.current_y_position = position[1]
        self.hit_time = 20

    def fly(self):
        bullet_points = []
        bullet_points.append((self.current_x_position, self.current_y_position))
        bullet_points.append((self.current_x_position + self.width, self.current_y_position))
        bullet_points.append((self.current_x_position + self.width, self.current_y_position + self.height))
        bullet_points.append((self.current_x_position, self.current_y_position + self.height))
        for enemy in enemy_list:
            enemy_current_x_position, enemy_current_y_position = enemy.get_current_position()
            for bullet in bullet_points:
                if bullet[0] >= enemy_current_x_position and bullet[1] >= enemy_current_y_position and bullet[0] <= enemy_current_x_position + enemy.width and bullet[1] <= enemy_current_y_position + enemy.height: # в метод общий
                    enemy.hit_time = self.hit_time
                    self.is_dead = True
        if self.current_x_position <= 0 or self.current_x_position >= screen.get_width() or self.current_y_position <= 0 or self.current_y_position >= screen.get_height():
            self.is_dead = True
        if not self.is_dead:
            if self.direction == 'UP':
                self.current_y_position -= self.bullet_speed
            elif  self.direction == 'DOWN':
                self.current_y_position += self.bullet_speed
            elif self.direction == 'LEFT':
                self.current_x_position -= self.bullet_speed
            elif self.direction == 'RIGHT':
                self.current_x_position += self.bullet_speed
            elif self.direction == 'RIGHT_UP':
                self.current_x_position += self.bullet_speed
                self.current_y_position -= self.bullet_speed
            elif self.direction == 'RIGHT_DOWN':
                self.current_x_position += self.bullet_speed
                self.current_y_position += self.bullet_speed
            elif self.direction == 'LEFT_UP':
                self.current_x_position -= self.bullet_speed
                self.current_y_position -= self.bullet_speed
            elif self.direction == 'LEFT_DOWN':
                self.current_x_position -= self.bullet_speed
                self.current_y_position += self.bullet_speed

        return self.current_x_position, self.current_y_position, self.width, self.height



class ColoredPoints():
    list_of_enemy_positions = []
    enemy_start_positions = []


    def __init__(self, is_hero=False, is_last=False):
        unique_start_y_position = False
        self.enemy_speed = 10
        self.is_hero = is_hero
        self.width = 100
        self.height = 100
        self.current_x_position = 0 if is_hero else screen.get_width() - self.width
        self.current_y_position = ColoredPoints.calc_start_y_position(is_hero)
        self.type_of_enemy = 2 if is_last else randint(1, 2)
        self.is_last = is_last
        self.x_is_achivied = False
        self.hit_time = 0

    def calc_start_y_position(is_hero):
        unique_start_y_position = False
        enemy_start_positions = []
        if is_hero:
            return randint(0, screen.get_height())
        else:
            while unique_start_y_position == False:
                new_y_position = randint(0, screen.get_height())
                if not ColoredPoints.enemy_start_positions:
                    enemy_start_positions.append(new_y_position)
                    unique_start_y_position = True
                    return new_y_position
                else:
                    for y_position in ColoredPoints.enemy_start_positions:
                        if abs(new_y_position - y_position) > self.height:
                            ColoredPoints.enemy_start_positions.append(new_y_position)
                            ColoredPoints.unique_start_y_position = True
                            return new_y_position

    def current_position(self, x_speed, y_speed):
        if 0 <= self.current_x_position + x_speed < screen.get_width() - self.width:
            self.current_x_position += x_speed
        elif self.current_x_position + x_speed < 0:
            self.current_x_position = 0
        else:
            self.current_x_position = screen.get_width() - self.width
        if 0 <= self.current_y_position + y_speed < screen.get_height() - self.height:
            self.current_y_position += y_speed
        elif self.current_y_position + y_speed < 0:
            self.current_y_position = 0
        else:
            self.current_y_position = screen.get_height() - self.height

        return self.current_x_position, self.current_y_position

    def enemy_position(self, hero):
        source_x_position = self.current_x_position
        source_y_position = self.current_y_position
        if self.hit_time != 0:
            self.hit_time -= 1
            return self.current_x_position, self.current_y_position
        if self.type_of_enemy == 2:
            if self.current_x_position >= hero.current_x_position:
                x_equal = True if self.current_x_position - self.enemy_speed <= hero.current_x_position else False
            elif self.current_x_position <= hero.current_x_position:
                x_equal = True if self.current_x_position + self.enemy_speed >= hero.current_x_position + hero.width else False
            if self.current_y_position >= hero.current_y_position:
                y_equal = True if self.current_y_position - self.enemy_speed <= hero.current_y_position else False
            elif self.current_y_position <= hero.current_y_position:
                y_equal = True if self.current_y_position + self.enemy_speed >= hero.current_y_position + hero.height else False
            if not x_equal and not y_equal:
                if hero.current_x_position < self.current_x_position and hero.current_y_position < self.current_y_position:
                    self.current_x_position -= self.enemy_speed
                    self.current_y_position -= self.enemy_speed

                elif hero.current_x_position > self.current_x_position and hero.current_y_position > self.current_y_position:
                    self.current_x_position += self.enemy_speed
                    self.current_y_position += self.enemy_speed

                elif hero.current_x_position < self.current_x_position and hero.current_y_position > self.current_y_position:
                    self.current_x_position -= self.enemy_speed
                    self.current_y_position += self.enemy_speed

                elif hero.current_x_position > self.current_x_position and hero.current_y_position < self.current_y_position:
                    self.current_x_position += self.enemy_speed
                    self.current_y_position -= self.enemy_speed

            elif x_equal and not y_equal:
                self.current_x_position = hero.current_x_position
                if self.current_y_position < hero.current_y_position:
                    self.current_y_position += self.enemy_speed

                else:
                    self.current_y_position -= self.enemy_speed


            elif not x_equal and y_equal:
                self.current_y_position = hero.current_y_position
                if self.current_x_position < hero.current_x_position:
                    self.current_x_position += self.enemy_speed

                else:
                    self.current_x_position -= self.enemy_speed

            elif x_equal and y_equal:
                self.current_y_position = hero.current_y_position
                self.current_x_position = hero.current_x_position

            if ColoredPoints.list_of_enemy_positions:

                for pos in ColoredPoints.list_of_enemy_positions:
                    if abs(pos[0] - self.current_x_position) <= self.width and abs(
                            pos[1] - self.current_y_position) <= self.height:
                        self.current_x_position = source_x_position
                        self.current_y_position = source_y_position
            ColoredPoints.list_of_enemy_positions.append((self.current_x_position, self.current_y_position))
            if self.is_last:
                ColoredPoints.list_of_enemy_positions.clear()
        else:
            if not self.x_is_achivied:
                if self.current_x_position - self.enemy_speed != 0:
                    self.current_x_position -= self.enemy_speed
                else:
                    self.current_x_position = 0
                    self.x_is_achivied = True
            else:
                if self.current_x_position + self.enemy_speed != screen.get_width() - self.width:
                    self.current_x_position += self.enemy_speed
                else:
                    self.current_x_position = screen.get_width() - self.width
                    self.x_is_achivied = False


        return self.current_x_position, self.current_y_position

    def get_current_position(self):
        return self.current_x_position, self.current_y_position


    def win():
        if hero.current_x_position + hero.width == screen.get_width():
            return True

    def lose():
        hero_top_left_corner = hero.current_x_position, hero.current_y_position
        hero_bottom_right_corner = hero.current_x_position + hero.width, hero.current_y_position + hero.height
        for enemy in enemy_list:
            points_list = []
            points_list.append((enemy.current_x_position, enemy.current_y_position))
            points_list.append((enemy.current_x_position + enemy.width, enemy.current_y_position))
            points_list.append((enemy.current_x_position + enemy.width, enemy.current_y_position + enemy.height))
            points_list.append((enemy.current_x_position, enemy.current_y_position + enemy.height))
            for point in points_list:
                if point[0] >= hero_top_left_corner[0] and point[1] >= hero_top_left_corner[1] and point[0] <=  hero_bottom_right_corner[0] and point[1] <= hero_bottom_right_corner[1]:
                    return True




BLACK = (0, 0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

pygame.init()

background = BLACK
screen = pygame.display.set_mode((1200, 1000))
hero = ColoredPoints(is_hero=True)
enemy_count = 3
enemy_list = []
bullet_list = []
for i in range(enemy_count):
    is_last = True if i == enemy_count - 1 else False
    enemy_list.append(ColoredPoints(is_last=is_last))
font = pygame.font.SysFont('consolas', 48)
img_win = font.render('You won', True, RED)
img_lose = font.render('You lose', True, RED)
hero_image = pygame.image.load(r'flag.jpeg')
hero_image = pygame.transform.scale(hero_image, (100, 100))
enemy_image = pygame.image.load(r'enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (100, 100))
BLACK = (0, 0, 0, 255)
x_speed, y_speed = 0, 0
default_x_speed, default_y_speed = 40, 40
running = True
win = False
lose = False
shoot_delay = 0
while running:
    shoot_delay += 1
    pygame.time.delay(50)
    screen.fill(background)
    hero_center = (hero.current_x_position + hero.width / 2, hero.current_y_position + hero.height / 2)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    # print(hero.current_x_position, hero.current_y_position)
    # for enemy in enemies_list:
    #     print('enemy:' + str(enemy.current_x_position) + ', ' + str(enemy.current_y_position))
    # print(lose)
    if lose:
        screen.fill(background)
        screen.blit(img_lose, (screen.get_width() / 2, screen.get_height() / 2))
    elif win:
        screen.fill(background)
        screen.blit(img_win, (screen.get_width() / 2, screen.get_height() / 2))
    else:
        if event.type == pygame.KEYUP:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('RIGHT_DOWN', hero_center))
        elif keys[pygame.K_SPACE] and keys[pygame.K_LEFT] and keys[pygame.K_DOWN] and keys[pygame.K_SPACE]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('LEFT_DOWN', hero_center))
        elif keys[pygame.K_SPACE] and keys[pygame.K_RIGHT] and keys[pygame.K_UP] and keys[pygame.K_SPACE]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('RIGHT_UP', hero_center))
        elif keys[pygame.K_SPACE] and keys[pygame.K_LEFT] and keys[pygame.K_UP] and keys[pygame.K_SPACE]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('LEFT_UP', hero_center))
        elif keys[pygame.K_SPACE] and keys[pygame.K_RIGHT]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('RIGHT', hero_center))
        elif keys[pygame.K_SPACE] and keys[pygame.K_LEFT]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('LEFT', hero_center))
        elif keys[pygame.K_SPACE] and keys[pygame.K_DOWN]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('DOWN', hero_center))
        elif keys[pygame.K_SPACE] and keys[pygame.K_UP]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('UP', hero_center))
        elif keys[pygame.K_SPACE] and keys[pygame.K_UP]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('UP', hero_center))
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] and keys[pygame.K_SPACE]:
            x_speed, y_speed = 1 * default_x_speed, 1 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('RIGHT_DOWN', hero_center))
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN] and keys[pygame.K_SPACE]:
            x_speed, y_speed = -1 * default_x_speed, 1 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('LEFT_DOWN', hero_center))
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP] and keys[pygame.K_SPACE]:
            x_speed, y_speed = 1 * default_x_speed, -1 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('RIGHT_UP', hero_center))
        elif keys[pygame.K_LEFT] and keys[pygame.K_UP] and keys[pygame.K_SPACE]:
            x_speed, y_speed = -1 * default_x_speed, -1 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('LEFT_UP', hero_center))
        elif keys[pygame.K_UP] and keys[pygame.K_SPACE]:
            x_speed, y_speed = 0 * default_x_speed, -1 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('UP', hero_center))
        elif keys[pygame.K_LEFT] and keys[pygame.K_SPACE]:
            x_speed, y_speed = -1 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('LEFT', hero_center))
        elif keys[pygame.K_RIGHT] and keys[pygame.K_SPACE]:
            x_speed, y_speed = 1 * default_x_speed, 0 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('RIGHT', hero_center))
        elif keys[pygame.K_DOWN] and keys[pygame.K_SPACE]:
            x_speed, y_speed = 0 * default_x_speed, 1 * default_y_speed
            if shoot_delay == 5:
                bullet_list.append(Bullet('DOWN', hero_center))
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            x_speed, y_speed = 1 * default_x_speed, 1 * default_y_speed
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            x_speed, y_speed = 1 * default_x_speed, -1 * default_y_speed
        elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            x_speed, y_speed = -1 * default_x_speed, -1 * default_y_speed
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            x_speed, y_speed = -1 * default_x_speed, 1 * default_y_speed
        elif keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
        elif keys[pygame.K_UP] and keys[pygame.K_DOWN]:
            x_speed, y_speed = 0 * default_x_speed, 0 * default_y_speed
        elif keys[pygame.K_LEFT]:
            x_speed, y_speed = -1 * default_x_speed, 0 * default_y_speed
        elif keys[pygame.K_RIGHT]:
            x_speed, y_speed = 1 * default_x_speed, 0 * default_y_speed
        elif keys[pygame.K_UP]:
            x_speed, y_speed = 0 * default_x_speed, -1 * default_y_speed
        elif keys[pygame.K_DOWN]:
            x_speed, y_speed = 0 * default_x_speed, 1 * default_y_speed
        screen.blit(hero_image, (hero.current_position(x_speed, y_speed)))
        for enemy in enemy_list:
            screen.blit(enemy_image, (enemy.enemy_position(hero)))
        for bullet in bullet_list:
            if not bullet.is_dead:
                pygame.draw.rect(screen, RED, (bullet.fly()))

    if shoot_delay == 5:
        shoot_delay = 0
    else:
        shoot_delay += 1
    if ColoredPoints.lose():
        lose = True

    if ColoredPoints.win():
        win = True

    pygame.display.update()

pygame.quit()
