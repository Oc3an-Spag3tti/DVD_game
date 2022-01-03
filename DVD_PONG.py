import pygame
from pygame import * 

pygame.init()

screen_width = 1920
screen_height = 1080
full_hd = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('DVD PONg')

background = (0, 0, 0)

brick_lvl_3 = (0,102,128)
brick_lvl_2 = (0,184,230)
brick_lvl_1 = (77,219,255)


player_color =  (115, 115, 115)
player_border = (179, 179, 179)


  
columns = 6
rows = 6
clock = pygame.time.Clock()
fps = 60

class edge():
    def __init__(self):
        self.width = screen_width // columns
        self.height = 50

    def create_edge(self):
        self.bricks = []

        brick_id = []
        for row in range(rows):

            brick_row = []
            for column in range(columns):

                brick_x = column * self.width
                brick_y = row * self.height
                rectangle = pygame.Rect(brick_x, brick_y, self.width, self.height)

                if row < 2:
                    hp = 3 
                elif row < 4:
                    hp = 2
                elif row < 6:
                    hp = 1
                
                brick_id = [rectangle, hp]

                brick_row.append(brick_id)

                self.bricks.append(brick_row)

    def appear_edge(self):
        for row in self.bricks:
            for brick in row:

                if brick[1]  == 3:
                    brick_color = brick_lvl_3

                elif brick[1]  == 2:
                    brick_color = brick_lvl_2

                elif brick[1]  == 1:
                    brick_color = brick_lvl_1

                pygame.draw.rect(full_hd, brick_color,brick[0])
                pygame.draw.rect(full_hd, background,brick[0], 2)

class player():
    def __init__(self):
        self.height = 20
        self.width = int(screen_width / columns)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 13
        self.rectange = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def move(self):

        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rectange.left > 0:
            self.rectange.x -= self.speed
            self.direction = - 1
        if key[pygame.K_RIGHT] and self.rectange.right < screen_width:
            self.rectange.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(full_hd, player_color, self.rectange)
        pygame.draw.rect(full_hd, player_border, self.rectange, 3)

class ball():
    def __init__(self, x, y):
        self



Edge = edge()
Edge.create_edge()

player_paddle = player()







running = True
while running:

    clock.tick(fps)
    full_hd.fill

    full_hd.fill(background)
     
    Edge.appear_edge()

    player_paddle.draw()
    player_paddle.move()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

