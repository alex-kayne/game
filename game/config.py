from random import randint


screen_size = (1200, 1000)
# width, height, speed, start_x_postition-start_y_position
hero_config = {'image': r'flag.jpeg', 'width': 100, 'height': 100, 'speed': 20, 'start_x_position': 0,
               'start_y_position': randint(0, screen_size[1])}
hero_image = r'flag.jpeg'
enemy_image = r'enemy.png'
list_of_enemy_positions = []
enemies_config = [ \
    {'image':r'1.png', 'width': 100, 'height': 100, 'speed': 10, 'start_x_position': screen_size[0], 'start_y_position': 100, 'hit_time': 5},
    {'image':r'2.png', 'width': 100, 'height': 100, 'speed': 10, 'start_x_position': screen_size[0], 'start_y_position': 400, 'hit_time': 5},
    {'image':r'3.png', 'width': 100, 'height': 100, 'speed': 10, 'start_x_position': screen_size[0], 'start_y_position': 900, 'hit_time': 5},
]
bullet_config = {'image': r'bullet.jpg', 'width': 10, 'height': 10, 'speed': 80, 'start_x_position': 0,
               'start_y_position': 0}
direction_list = {
    'UP': [0, -1],
    'DOWN': [0, 1],
    'LEFT': [-1, 0],
    'RIGHT': [1, 0],
    'STOP': [0, 0]
}

class Pomidoro:
    pass
