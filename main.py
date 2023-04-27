import data as data
import pygame
import self as self
from pygame.locals import*
pygame.mixer.init()
pygame.mixer.music.load('Chucky.mp3')
pygame.mixer.music.play()
pygame.init()
clock = pygame.time.Clock()
fps = 100
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption('Rocket man')
# Variable used in the game
tile_size = 30
game_over = 0
score = 0
bg_img = pygame.image.load('Convergence.png')
restart_img = pygame.image.load('restart_btn.png')

#Creating Grids on the game
#def draw_grid():
 #for line in range(0, 20):
  #pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
  #pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
  #creating a list and player to add items into the grid
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action




class Player:
    def __init__(self, x, y):
        self.reset(x, y)
    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 20
        if game_over == 0:
            # moving player
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -12
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 3
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 3
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #Handling animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            #gravity
            dy += self.vel_y
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10

            #check for collision
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            # checking for collision amongst enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
            # checking for collision amongst toxic waste
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            # checking for collision amongst recycling machine
            if pygame.sprite.spritecollide(self, Recycle_group, True):
                game_over = 1


            # update player coordinates/ stopping player from falling down
            self.rect.x += dx
            self.rect.y += dy
     #drawing the player on the screen
        screen.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


class World:
    def __init__(self, data):
        self.tile_list = []

        # load images and assigning number to the list below
        purpsss = pygame.image.load('reddd.png')
        wall_img = pygame.image.load('brickwall.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(purpsss, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    #tuple to store image and a rectangle around it
                    tile = (img, img_rect)
                    #append is used to add items to the list
                    self.tile_list.append(tile)

                if tile == 7:
                        img = pygame.transform.scale(wall_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size )
                    blob_group.add(blob)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 1))
                    lava_group.add(lava)
                if tile == 4:
                    garbage = Garbage(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    Garbage_group.add(garbage)
                if tile == 5:
                    rec_mach = Exit(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    Recycle_group.add(rec_mach)
                    #count is used to increase column and row count as images are added to the list
                col_count += 1
            row_count += 1

    #creation of tile and line thickness for colissions
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
#creating enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ghost2.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

#creating lava
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('lava3.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#creating garbage


class Garbage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('trashh.png')
        self.image = pygame.transform.scale(img, (tile_size // 1, tile_size // 1))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


#creating exit when the player reaches the recycling machine with garbage

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('rec3.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size *  2.5)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


#my list
world_data= [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 3, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 1],
[1, 4, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 1],
[1, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 1],
[1, 0, 0, 0, 0, 0, 7, 7, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
Player = Player(35, screen_height - 110)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
Garbage_group = pygame.sprite.Group()
Recycle_group = pygame.sprite.Group()
world = World(world_data)
#creating buttons for restarting
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)

#creating menu button rectangles
start_rect = pygame.Rect((screen_width/2 - 100, screen_height/2 - 50, 200, 100))
quit_rect = pygame.Rect((screen_width/2 - 100, screen_height/2 + 65, 200, 100))

def game_loop():
    global game_over, score
    #Loop to start and end the game(grid added,)
    run = True
    while run:
        clock.tick(fps)
        screen.blit(bg_img, (0, 0))

        world.draw()
        blob_group.update()
        # update score
        #check if a garbage bag has been collected
        if pygame.sprite.spritecollide(Player, Garbage_group, True):
            score  = score + 1
            print(score)

        blob_group.draw(screen)
        lava_group.draw(screen)
        Garbage_group.draw(screen)
        Recycle_group.draw(screen)

        game_over= Player.update(game_over)

        if game_over == -1:
            if restart_button.draw():
                Player.reset(35, screen_height - 110)
                game_over = 0
                score = 0

        # draw_grid()

        for event in pygame.event.get():
            #screen.blit(crys_img, (100, 100))
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()

# creating start menu
def draw_start_menu():
    global start_rect, quit_rect 
    menu_bg_image = pygame.image.load("recycle-rush.png")
    screen.blit(menu_bg_image, (0, 0))

    start_image = pygame.image.load("start-image.png")
    screen.blit(start_image, start_rect)

    quit_image = pygame.image.load("quit-image.png")
    screen.blit(quit_image, quit_rect)

draw_start_menu()
#QUIT is used to close the window of the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_rect.collidepoint(mouse_pos):
                game_loop()
            elif quit_rect.collidepoint(mouse_pos):
                pygame.quit()

    pygame.display.update()


