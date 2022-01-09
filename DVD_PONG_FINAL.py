import pygame
from pygame.locals import * 

pygame.init()

#dimentions de l'ecran
screen_width = 1920
screen_height = 1080
full_hd = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('DVD PONg')

background = (240, 216, 120)

#coouleur des briques
brick_lvl_1 =   (76, 201, 240)
brick_lvl_2 =   (46, 196, 182)
brick_lvl_3 =  (39, 125, 161)


player_color =  (192, 96, 72)
player_border =  (0, 72, 120)

txt_color = (45, 49, 66)
txt_font = pygame.font.Font('D:\daniil.py\PROJET NSI FIN JANVIER\Paskowy.TTF', 100)

#dimention du mur des briques  
columns = 10
rows = 10
clock = pygame.time.Clock()
fps = 60
live = False
game_over = 0

def write_txt(txt, txt_font, txt_color, x, y):
    img = txt_font.render(txt, True, txt_color)
    full_hd.blit(img, (x, y))

#classe des briques represntees par des listes des listes
class edge():
    def __init__(self):
        self.width = screen_width // columns
        self.height = 50

    def create_edge(self):
        self.bricks = []
         
        brick_id = []
        for row in range(rows):
             
            brick_row = []
             
            for col in range(columns):
                 
                brick_x = col * self.width
                brick_y = row * self.height
                rect = pygame.Rect(brick_x, brick_y, self.width, self.height)
#points de vies de briques                 
                if row < 3:
                    lives = 3
                elif row < 6:
                    lives = 2
                elif row < 9:
                    lives = 1
                 
                brick_id = [rect, lives]
                 
                brick_row.append(brick_id)
            
            self.bricks.append(brick_row)

#appaitre le mur des briques
    def appear_edge(self):
        for row in self.bricks:
            for brick in row:

                if brick[1] == 3:
                    brick_color = brick_lvl_3
                elif brick[1] == 2:
                    brick_color = brick_lvl_2
                elif brick[1] == 1:
                    brick_color = brick_lvl_1
                pygame.draw.rect(full_hd, brick_color, brick[0])
                pygame.draw.rect(full_hd, background, (brick[0]), 2)

# la classe joueur

class player():
    def __init__(self):
        self.revive()
#bouger
    def move(self):

        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1
#apparaitre
    def appeared(self):
        pygame.draw.rect(full_hd, player_color, self.rect)
        pygame.draw.rect(full_hd, player_border, self.rect, 3)

#lorsque le jeu est fini le jour se place a la position initiale
    def revive(self):
        self.height = 20
        self.width = int(screen_width / columns)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 13
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

#c'est le logo dvd de base qui fait la fonctino s'une balle mais maintenant c'est juste la balle

class dvd():
    def __init__(self, x, y):
        self.revive(x, y)

#la methode la plus complique car la balle bouge dans dans tout les sens et rebondisse mais c'est qui est complique c'est que lorque elle rebondisse elle doit dtruire la brique
    def do_magic(self):
        collision = 5
        edge_destroyed = 1
        row_counter = 0
        for row in Edge.bricks:
            item_counter = 0
            for item in row:
            #verfier si elle rebondisse
                if self.rect.colliderect(item[0]):
                     
                    if abs(self.rect.bottom - item[0].top) < collision and self.speed_y > 0:
                        self.speed_y *= -1
                     
                    if abs(self.rect.top - item[0].bottom) < collision and self.speed_y < 0:
                        self.speed_y *= -1                      
                   
                    if abs(self.rect.right - item[0].left) < collision and self.speed_x > 0:
                        self.speed_x *= -1
                    
                    if abs(self.rect.left - item[0].right) < collision and self.speed_x < 0:
                        self.speed_x *= -1
                     
                    if Edge.bricks[row_counter][item_counter][1] > 1:
                        Edge.bricks[row_counter][item_counter][1] -= 1
                    else:
                        Edge.bricks[row_counter][item_counter][0] = (0, 0, 0, 0)

                 
                if Edge.bricks[row_counter][item_counter][0] != (0, 0, 0, 0):
                    edge_destroyed = 0
                 
                item_counter += 1
             
            row_counter += 1
 
        if edge_destroyed == 1:
            self.game_over = 1


        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

   
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.over = -1


 
        if self.rect.colliderect(player_paddle):
 
            if abs(self.rect.bottom - player_paddle.rect.top) < collision and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1



        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.over

#apparaitre la balle
    def appear(self):
        pygame.draw.circle(full_hd, player_color, (self.rect.x + self.ray, self.rect.y + self.ray), self.ray)
        pygame.draw.circle(full_hd, player_border, (self.rect.x + self.ray, self.rect.y + self.ray), self.ray, 3)

#meme methode comme pour joueur
    def revive(self, x, y):
        self.ray = 15
        self.x = x - self.ray
        self.y = y
        self.rect = Rect(self.x, self.y, self.ray * 2, self.ray * 2)
        self.speed_x = 7  
        self.speed_y = -7
        self.speed_max = 8
        self.over = 0




Edge = edge()
Edge.create_edge()

player_paddle = player()

ball_dvd =  dvd(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)




#pour tourner le jeu

running = True
while running:

    clock.tick(fps)
    full_hd.fill

    full_hd.fill(background)
     
    Edge.appear_edge()
    player_paddle.appeared()
    ball_dvd.appear()

    if live:
                    
        
        player_paddle.move()
        game_over = ball_dvd.do_magic()
        if game_over !=0:
            live = False

    if not live:
        if game_over == 0:
            write_txt('CLIQUEZ POUR COMMENCER', txt_font, txt_color, 750,  screen_height // 2 + 100)
        elif game_over == 1:
            write_txt('2EZ !', txt_font, txt_color, 750, screen_height // 2 + 50)
        elif game_over == -1:
            write_txt('TU DOIS TRY HARD !', txt_font, txt_color, 750, screen_height // 2 + 50)
     


 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and live == False:
            live = True
            ball_dvd.revive(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.revive()
            Edge.create_edge()
    
    pygame.display.update()

