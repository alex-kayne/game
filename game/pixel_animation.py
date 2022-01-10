import pygame
from pygame.locals import *
import time
from random import randint

class ColoredPoints():
    global speed_width
    global speed_height # global это очень плохо
    speed_width = 1
    speed_height = 1
    def __init__(self, width, height):
        self.source_height = height
        self.source_width = width
        self.current_height = randint(0, 500)
        self.current_width = randint(0, 1000)

    def change_current_position(self):
        if self.source_height != self.current_height:
            if self.source_height < self.current_height:
                self.current_height -= speed_height
            elif self.source_height > self.current_height:
                self.current_height += speed_height
        if self.source_width != self.current_width:
            if self.source_width < self.current_width:
                self.current_width -= speed_width
            elif self.source_width > self.current_width:
                self.current_width += speed_width
        return self.current_width, self.current_height, 1, 1

BLACK = (0, 0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((1000, 500))
# print(pygame.font.get_fonts())

font = pygame.font.SysFont('consolas', 48)
img = font.render('Gleb Jirniy', True, RED)
# print(img.get_size())
# print(type(img.get_size()))
# print(img.get_buffer)

running = True
background = BLACK
screen.blit(img, (320, 212))

height, width = img.get_size()[1], img.get_size()[0]
points_object_list = []
for i in range(width):
    for l in range(height):
        if screen.get_at((320 + i, 212 + l)) != BLACK:

            points_object_list.append(ColoredPoints(320 + i, 212 + l))


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(background)
    is_finished = False
    for i in points_object_list:
        pygame.draw.rect(screen, RED, (i.change_current_position()))

    pygame.display.update()

pygame.quit()