import pygame
from pygame.locals import *
import time
from random import randint
from abc import ABC, abstractmethod
import config
from config import direction_list
from config import bullet_config
from itertools import combinations


class GameObjects(ABC):
    def __init__(self, **attributes):
        self.width = attributes['width']
        self.height = attributes['height']
        self.speed = attributes['speed']
        self.current_x_position = attributes['start_x_position']
        self.current_y_position = attributes['start_y_position']
        self.image = pygame.image.load(attributes['image'])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.is_dead = False
        self.source_x_position = attributes['start_x_position']
        self.source_y_position = attributes['start_y_position']

    @abstractmethod
    def move(self):
        pass

    def get_image(self):
        return self.image

    def get_current_position(self):
        return self.current_x_position, self.current_y_position

    def get_source_position(self):
        return self.source_x_position, self.source_y_position

    def get_width_and_height(self):
        return self.width, self.height

    def get_is_dead(self):
        return self.is_dead

    def get_speed(self):
        return self.speed

    def set_current_position_via_speed(self, x_speed=0, y_speed=0):
        self.current_x_position += x_speed
        self.current_y_position += y_speed

    def set_current_position(self, x_position, y_position):
        self.current_x_position = x_position if x_position != None else self.current_x_position
        self.current_y_position = y_position if y_position != None else self.current_y_position

    def set_is_dead(self, is_dead):
        self.is_dead = is_dead



class Bullet(GameObjects):
    def __init__(self, **attributes):
        self.width = attributes['width']
        self.height = attributes['height']
        self.speed = attributes['speed']
        self.current_x_position = attributes['start_x_position']
        self.current_y_position = attributes['start_y_position']
        self.image = pygame.image.load(attributes['image'])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.is_dead = False
        self.directions = attributes['directions']
        self.calc_speed(self.directions)

    def calc_speed(self, directions):
        final_speed = []
        for direction in directions:
            if not final_speed:
                final_speed = direction_list[direction]
            else:
                final_speed = [final_speed[0] + direction_list[direction][0],
                               final_speed[1] + direction_list[direction][1]]
        self.speed = self.speed * final_speed[0], self.speed * final_speed[1]

    def move(self):

        self.current_x_position, self.current_y_position = self.current_x_position + self.speed[
            0], self.current_y_position + self.speed[1]
        if self.current_x_position < 0 or self.current_x_position > screen.get_width():
            self.is_dead = True
        if self.current_y_position < 0 or self.current_y_position > screen.get_height():
            self.is_dead = True


class Enemy(GameObjects):

    def __init__(self, **attributes):
        self.width = attributes['width']
        self.height = attributes['height']
        self.speed = attributes['speed']
        self.current_x_position = attributes['start_x_position']
        self.current_y_position = attributes['start_y_position']
        self.image = pygame.image.load(attributes['image'])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.is_dead = False
        self.source_x_position = attributes['start_x_position']
        self.source_y_position = attributes['start_y_position']
        self.stacked_time = 0
        self.hit_time = attributes['hit_time']

    def move(self, hero):
        self.source_x_position = self.current_x_position
        self.source_y_position = self.current_y_position
        hero_current_x_position, hero_current_y_position = hero.get_current_position()
        hero_width, hero_height = hero.get_width_and_height()

        if self.stacked_time != 0:
            self.stacked_time -= 1
        else:
            if self.current_x_position >= hero_current_x_position:
                x_equal = True if self.current_x_position - self.speed <= hero_current_x_position else False
            elif self.current_x_position <= hero.current_x_position:
                x_equal = True if self.current_x_position + self.speed >= hero_current_x_position + hero_width else False
            if self.current_y_position >= hero.current_y_position:
                y_equal = True if self.current_y_position - self.speed <= hero_current_y_position else False
            elif self.current_y_position <= hero.current_y_position:
                y_equal = True if self.current_y_position + self.speed >= hero_current_y_position + hero_height else False
            if not x_equal and not y_equal:
                if hero.current_x_position < self.current_x_position and hero_current_y_position < self.current_y_position:
                    self.current_x_position -= self.speed
                    self.current_y_position -= self.speed

                elif hero_current_x_position > self.current_x_position and hero_current_y_position > self.current_y_position:
                    self.current_x_position += self.speed
                    self.current_y_position += self.speed

                elif hero_current_x_position < self.current_x_position and hero_current_y_position > self.current_y_position:
                    self.current_x_position -= self.speed
                    self.current_y_position += self.speed

                elif hero_current_x_position > self.current_x_position \
                        and hero_current_y_position < self.current_y_position:
                    self.current_x_position += self.speed
                    self.current_y_position -= self.speed

            elif x_equal and not y_equal:
                self.current_x_position = hero_current_x_position
                if self.current_y_position < hero_current_y_position:
                    self.current_y_position += self.speed

                else:
                    self.current_y_position -= self.speed


            elif not x_equal and y_equal:
                self.current_y_position = hero_current_y_position
                if self.current_x_position < hero_current_x_position:
                    self.current_x_position += self.speed

                else:
                    self.current_x_position -= self.speed

            elif x_equal and y_equal:
                self.current_y_position = hero_current_y_position
                self.current_x_position = hero_current_x_position

    def set_stacked_time(self):
        self.stacked_time = self.hit_time

class Hero(GameObjects):

    def move(self, *direction_tuple):
        final_speed = []
        if direction_tuple == 'STOP':
            x_speed, y_speed = 0, 0
        else:
            for direction in direction_tuple:
                if not final_speed:
                    final_speed = direction_list[direction]

                else:
                    final_speed = [final_speed[0] + direction_list[direction][0],
                                   final_speed[1] + direction_list[direction][1]]
            x_speed, y_speed = self.speed * final_speed[0], self.speed * final_speed[1]

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


def crossing(**all_objects):
    hero = all_objects['hero']
    enemies_list = all_objects['enemies_list']
    bullets_list = all_objects['bullets_list']
    hero_current_x_position, hero_current_y_position = hero.get_current_position()
    for enemy1, enemy2 in combinations(enemies_list, 2):
        enemy1_current_x_position, enemy1_current_y_position = enemy1.get_current_position()
        enemy2_current_x_position, enemy2_current_y_position = enemy2.get_current_position()
        enemy1_source_x_position, enemy1_source_y_position = enemy1.get_source_position()
        enemy2_source_x_position, enemy2_source_y_position = enemy2.get_source_position()
        enemy1_width, enemy1_height = enemy1.get_width_and_height()
        enemy2_width, enemy2_height = enemy2.get_width_and_height()


        enemy1_is_faster = ((hero_current_x_position - enemy1_current_x_position) ** 2 + (hero_current_y_position - enemy1_current_y_position) ** 2) ** 0.5 <= ((hero_current_x_position - enemy2_current_x_position) ** 2 + (hero_current_y_position - enemy2_current_y_position) ** 2) ** 0.5
        top_left = enemy1_current_x_position >= enemy2_current_x_position and enemy1_current_y_position >= enemy2_current_y_position \
            and enemy1_current_x_position <= enemy2_current_x_position + enemy2_width and enemy1_current_y_position <= enemy2_current_y_position + enemy2_width
        top_right = enemy1_current_x_position + enemy1_width >= enemy2_current_x_position and enemy1_current_y_position >= enemy2_current_y_position \
                            and enemy1_current_x_position + enemy1_width <= enemy2_current_x_position + enemy2_width and enemy1_current_y_position <= enemy2_current_y_position + enemy2_height
        left_bottom = enemy1_current_x_position >= enemy2_current_x_position and enemy1_current_y_position + enemy1_height >= enemy2_current_y_position \
                            and enemy1_current_x_position <= enemy2_current_x_position + enemy2_width and enemy1_current_y_position + enemy1_height <= enemy2_current_y_position + enemy2_height
        right_bottom = enemy1_current_x_position + enemy1_width>= enemy2_current_x_position and enemy1_current_y_position + enemy1_height >= enemy2_current_y_position \
                            and enemy1_current_x_position + enemy1_width <= enemy2_current_x_position + enemy2_width and enemy1_current_y_position + enemy1_height <= enemy2_current_y_position + enemy2_height
        if (left_bottom and right_bottom) or (left_bottom and right_bottom):
            if enemy1_is_faster:
                enemy1.set_current_position(enemy1_current_x_position, enemy1_source_y_position)
                enemy2.set_current_position(enemy2_source_x_position, enemy2_source_y_position)
            else:
                enemy2.set_current_position(enemy2_current_x_position,enemy2_source_y_position)
                enemy1.set_current_position(enemy1_source_x_position, enemy1_source_y_position)
        elif left_bottom and top_left:
            if enemy1_is_faster:
                enemy2.set_current_position(enemy2_source_x_position, enemy2_source_y_position)
            else:
                enemy2.set_current_position(enemy2_source_x_position, enemy2_source_y_position)
        elif top_left or top_right or right_bottom or left_bottom:
            if enemy1_is_faster:
                enemy2.set_current_position(enemy2_source_x_position, enemy2_source_y_position)
            else:
                enemy1.set_current_position(enemy1_source_x_position, enemy1_source_y_position)

# Определение мервтого героя
    hero_width, hero_height = hero.get_width_and_height()
    hero_top_left_corner = hero_current_x_position, hero_current_y_position
    hero_bottom_right_corner = hero_current_x_position + hero_width, hero_current_y_position + hero_height
    for enemy in enemies_list:
        enemy_current_x_position, enemy_current_y_position = enemy.get_current_position()
        enemy_width, enemy_height = enemy.get_width_and_height()
        points_list = []
        points_list.append((enemy_current_x_position, enemy_current_y_position))
        points_list.append((enemy_current_x_position + enemy_width, enemy_current_y_position))
        points_list.append((enemy_current_x_position + enemy_width, enemy_current_y_position + enemy_height))
        points_list.append((enemy_current_x_position, enemy_current_y_position + enemy_height))
        for point in points_list:
            if point[0] >= hero_top_left_corner[0] and point[1] >= hero_top_left_corner[1] and point[0] <= \
                    hero_bottom_right_corner[0] and point[1] <= hero_bottom_right_corner[1]:
                hero.set_is_dead(True)

        for bullet in bullets_list:
            if not bullet.get_is_dead():
                bullet_current_x_position, bullet_current_y_position = bullet.get_current_position()
                bullet_width, bullet_height = bullet.get_width_and_height()
                bullet_top_left_corner = bullet_current_x_position, bullet_current_y_position
                bullet_bottom_right_corner = bullet_current_x_position + bullet_width, bullet_current_y_position + bullet_height
                if points_list[0][0] <= bullet_top_left_corner[0] and points_list[0][1] <= bullet_top_left_corner[1] and points_list[2][0] >= \
                        bullet_bottom_right_corner[0] and points_list[2][1] >= bullet_bottom_right_corner[1]:
                    enemy.set_stacked_time()
                    bullet.set_is_dead(True)


# Определение застрявшего врага


def win(hero, screen_width):
    hero_current_x_position, hero_current_y_position = hero.get_current_position()
    hero_width, hero_height = hero.get_width_and_height()
    if hero_current_x_position + hero_width == screen_width:
        return True




RED = (255, 0, 0)
BLACK = (0, 0, 0, 255)
pygame.init()
background = BLACK
font = pygame.font.SysFont('consolas', 48)

screen = pygame.display.set_mode(config.screen_size)
hero = Hero(image=config.hero_config['image'], width=config.hero_config['width'], height=config.hero_config['height'],
            speed=config.hero_config['speed'], start_x_position=config.hero_config['start_x_position'],
            start_y_position=config.hero_config['start_y_position'] if config.hero_config['start_y_position'] <
                                                                       config.screen_size[1] - config.hero_config[
                                                                           'height'] else config.hero_config[
                                                                                              'start_y_position'] -
                                                                                          config.hero_config[
                                                                                              'height'])
enemies_list = []
for config in config.enemies_config:
    enemy = Enemy(image=config['image'], width=config['width'], height=config['height'], speed=config['speed'],
                  start_x_position=config['start_x_position'] - config['width'],
                  start_y_position=config['start_y_position'], hit_time=config['hit_time'])
    enemies_list.append(enemy)
runnig = True
bullets_list = []
while runnig:
    pygame.time.delay(50)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    keys = pygame.key.get_pressed()
    if win(hero, screen.get_width()):
        img_win = font.render('You won', True, RED)
        screen.fill(background)
        screen.blit(img_win, (screen.get_width() / 2, screen.get_height() / 2))
    else:
        if not hero.get_is_dead():
            if event.type == pygame.KEYUP:
                hero.move('STOP')
            if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] and keys[pygame.K_SPACE]:
                hero.move('RIGHT', 'DOWN')
                bullets_list.append(
                    Bullet(image=bullet_config['image'], width=bullet_config['width'], height=bullet_config['height'],
                           speed=bullet_config['speed'],
                           start_x_position=hero.get_current_position()[0] + hero.get_width_and_height()[0] / 2,
                           start_y_position=hero.get_current_position()[1] + hero.get_width_and_height()[1] / 2,
                           directions=['DOWN', 'RIGHT']))
            elif keys[pygame.K_RIGHT] and keys[pygame.K_UP] and keys[pygame.K_SPACE]:
                hero.move('RIGHT', 'UP')
                bullets_list.append(
                    Bullet(image=bullet_config['image'], width=bullet_config['width'], height=bullet_config['height'],
                           speed=bullet_config['speed'],
                           start_x_position=hero.get_current_position()[0] + hero.get_width_and_height()[0] / 2,
                           start_y_position=hero.get_current_position()[1] + hero.get_width_and_height()[1] / 2,
                           directions=['UP', 'RIGHT']))
            elif keys[pygame.K_LEFT] and keys[pygame.K_UP] and keys[pygame.K_SPACE]:
                hero.move('LEFT', 'UP')
                bullets_list.append(
                    Bullet(image=bullet_config['image'], width=bullet_config['width'], height=bullet_config['height'],
                           speed=bullet_config['speed'],
                           start_x_position=hero.get_current_position()[0] + hero.get_width_and_height()[0] / 2,
                           start_y_position=hero.get_current_position()[1] + hero.get_width_and_height()[1] / 2,
                           directions=['LEFT', 'UP']))
            elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN] and keys[pygame.K_SPACE]:
                hero.move('LEFT', 'DOWN')
                bullets_list.append(
                    Bullet(image=bullet_config['image'], width=bullet_config['width'], height=bullet_config['height'],
                           speed=bullet_config['speed'],
                           start_x_position=hero.get_current_position()[0] + hero.get_width_and_height()[0] / 2,
                           start_y_position=hero.get_current_position()[1] + hero.get_width_and_height()[1] / 2,
                           directions=['DOWN', 'LEFT']))
            elif keys[pygame.K_LEFT] and keys[pygame.K_SPACE]:
                hero.move('LEFT')
                bullets_list.append(
                    Bullet(image=bullet_config['image'], width=bullet_config['width'], height=bullet_config['height'],
                           speed=bullet_config['speed'],
                           start_x_position=hero.get_current_position()[0] + hero.get_width_and_height()[0] / 2,
                           start_y_position=hero.get_current_position()[1] + hero.get_width_and_height()[1] / 2,
                           directions=['LEFT']))
            elif keys[pygame.K_RIGHT] and keys[pygame.K_SPACE]:
                hero.move('RIGHT')
                bullets_list.append(
                    Bullet(image=bullet_config['image'], width=bullet_config['width'], height=bullet_config['height'],
                           speed=bullet_config['speed'],
                           start_x_position=hero.get_current_position()[0] + hero.get_width_and_height()[0] / 2,
                           start_y_position=hero.get_current_position()[1] + hero.get_width_and_height()[1] / 2,
                           directions=['RIGHT']))
            elif keys[pygame.K_UP] and keys[pygame.K_SPACE]:
                hero.move('UP')
                bullets_list.append(
                    Bullet(image=bullet_config['image'], width=bullet_config['width'], height=bullet_config['height'],
                           speed=bullet_config['speed'],
                           start_x_position=hero.get_current_position()[0] + hero.get_width_and_height()[0] / 2,
                           start_y_position=hero.get_current_position()[1] + hero.get_width_and_height()[1] / 2,
                           directions=['UP']))
            elif keys[pygame.K_DOWN] and keys[pygame.K_SPACE]:
                hero.move('DOWN')
                bullets_list.append(
                    Bullet(image=bullet_config['image'], width=bullet_config['width'], height=bullet_config['height'],
                           speed=bullet_config['speed'],
                           start_x_position=hero.get_current_position()[0] + hero.get_width_and_height()[0] / 2,
                           start_y_position=hero.get_current_position()[1] + hero.get_width_and_height()[1] / 2,
                           directions=['DOWN']))
            elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
                hero.move('RIGHT', 'DOWN')
            elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
                hero.move('RIGHT', 'UP')
            elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                hero.move('LEFT', 'UP')
            elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                hero.move('LEFT', 'DOWN')
            elif keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                hero.move('LEFT', 'RIGHT')
            elif keys[pygame.K_UP] and keys[pygame.K_DOWN]:
                hero.move('UP', 'DOWN')
            elif keys[pygame.K_LEFT]:
                hero.move('LEFT')
            elif keys[pygame.K_RIGHT]:
                hero.move('RIGHT')
            elif keys[pygame.K_UP]:
                hero.move('UP')
            elif keys[pygame.K_DOWN]:
                hero.move('DOWN')
            for enemy in enemies_list:
                enemy.move(hero)
            for bullet in bullets_list:
                if not bullet.get_is_dead():
                    bullet.move()
            crossing(hero=hero, enemies_list=enemies_list, bullets_list=bullets_list)

            # Отображение
            screen.blit(hero.get_image(), (hero.get_current_position()))
            for enemy in enemies_list:
                screen.blit(enemy.get_image(), enemy.get_current_position())
            for bullet in bullets_list:
                if not bullet.get_is_dead():
                    screen.blit(bullet.get_image(), bullet.get_current_position())
        else:
            img_lose = font.render('You lose', True, RED)
            screen.fill(background)
            screen.blit(img_lose, (screen.get_width() / 2, screen.get_height() / 2))

    pygame.display.update()
