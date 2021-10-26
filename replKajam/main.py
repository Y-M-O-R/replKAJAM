import csv
import sys
import os.path
import pygame



pygame.init()

# screen
screen_width, screen_height = 960, 640
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


class Boundary:
    def __init__(self, bound_screen):
        self.screen = bound_screen.get_rect()
        self.left_height = pygame.Rect((0, 0, 1, self.screen.height))
        self.top_width = pygame.Rect((0, 0, self.screen.width, 1))
        self.right_height = pygame.Rect((self.screen.width - 1, 0, 1, self.screen.height))
        self.bottom_width = pygame.Rect((0, self.screen.height - 1, self.screen.width, 1))
        self.bound_list = [self.left_height, self.top_width, self.right_height, self.bottom_width]


screen_border = Boundary(screen)


def quit_game():
    for event in pygame.event.get():  # loop to quit game

        if event.type == pygame.QUIT:  # fix this
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, img, img_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        # img_rect = pygame.Rect(img_rect)
        img_rect.append(64)
        img_rect.append(64)
        self.rect = pygame.Rect(img_rect)

def level_reader():
    sprite_list = [
        pygame.image.load(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\level\Background'
                          r'\Blue.png'),
        pygame.image.load(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\level\Background'
                          r'\Brown.png'),
        pygame.image.load(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\level\Background'
                          r'\Gray.png'),
        pygame.image.load(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\level\Background'
                          r'\Green.png'),
        pygame.image.load(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\level\Background'
                          r'\Pink.png'),
        pygame.image.load(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\level\Background'
                          r'\Purple.png'),
        pygame.image.load(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\level\Background'
                          r'\Yellow.png'),
    ]
    with open('level.csv', 'r') as csv_file:
        obstacle_sprite = pygame.sprite.Group()
        csv_reader = csv.reader(csv_file)
        for sprite in csv_reader:
            #print(sprite)
            sprite = list(map(int, sprite))
            img = sprite.pop(0)
            img_draw = Obstacle(sprite_list[img], sprite)
            obstacle_sprite.add(img_draw)
            #print(img, sprite)
           #  screen.blit(sprite_list[img], sprite)
        return  obstacle_sprite


obstacle_sprite = level_reader()





class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # scale sprite
        image = pygame.transform.scale(image,(500,500))

        # Assuming black works as the transparent color
        ##image.set_colorkey((0, 0, 0))
        transColor = image.get_at((0, 0))
        image.set_colorkey(transColor)

        # Return the image
        return image  # , a

class Background:
    def __init__(self):
        self.sprite_sheet = SpriteSheet(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\background\earth.png')
        self.sprite_list = []
        self.sprite_x_row = 0
        self.sprite_y_column = 0
        self.column_length = 9
        self.sprite_total = 0

        for sprite in range(70):
            self.sprite_list.append(self.sprite_sheet.get_image(self.sprite_x_row, self.sprite_y_column, 99, 99))
            self.sprite_x_row += 99
            if sprite >= self.column_length:
                self.sprite_y_column += 99
                self.column_length += 9
                self.sprite_x_row = 0

    def run_background(self):
        if self.sprite_total == 60:
            self.sprite_total = 0
        screen.blit(self.sprite_list[self.sprite_total], (screen_width//2- 250, screen_height//2-250))
                    #screen_width//2,screen_height//2
        self.sprite_total +=1




class Player(pygame.sprite.Sprite):

    def __init__(self, vel=5, health=5,
                 damage=1):  # sets x, y, width, height used for setting hit box
        super().__init__()

        self.vel = vel
        self.is_jump = False
        self.jump_count = 10
        self.health = health
        self.damage = damage
        self.left = False
        self.right = False

        self.position, self.velocity = pygame.math.Vector2(0,0)
        self.left_obsctacle_collision = False
        self.right_obsctacle_collision = False
        self.jump_obstacle_collision = False

        self.file_location = os.path.join('img', 'pixel_platformer_player')

        # animation for sprite
        self.walk_right_animation = [
            pygame.image.load(os.path.join(self.file_location, 'run', '1.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'run', '2.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'run', '3.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'run', '4.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'run', '5.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'run', '6.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'run', '7.png')).convert_alpha()
        ]

        self.walk_left_animation = []

        for image in self.walk_right_animation:
            self.walk_left_animation.append(pygame.transform.flip(image, True, False))

        self.jump_animation_right = [
            pygame.image.load(os.path.join(self.file_location, 'jump', '1.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'jump', '2.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'jump', '3.png')).convert_alpha()
        ]
        self.jump_animation_left = []

        for image in self.jump_animation_right:
            self.jump_animation_left.append(pygame.transform.flip(image, True, False))
        self.idle_animation = [
            pygame.image.load(os.path.join(self.file_location, 'idle', '1.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'idle', '2.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'idle', '3.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'idle', '4.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'idle', '5.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'idle', '6.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.file_location, 'idle', '7.png')).convert_alpha()
        ]
        self.idle_animation_left = []

        for image in self.idle_animation:
            self.idle_animation_left.append(pygame.transform.flip(image, True, False))

        self.walk_count = 0
        self.image = self.idle_animation[self.walk_count]

        self.rect = self.image.convert_alpha().get_rect()

        self.rect.midbottom = (screen_width // 2, screen_height)

        self.sprite_direction = True

    def check_health(self):
        if self.health <= 0:
            return True
        return False

    def display_hit_box(self):  # displays object hit box used for testing
        # (Surface.rect.width // 2, Surface.rect.height // 2)
        self.rectr = ((self.rect.x + 30, self.rect.y + 40), (35, 47.5))

        pygame.draw.rect(screen, (250, 0, 0), self.rect, 2)

        pygame.display.update()

    def create_rect(self):  # creates rect objects

        return self.rect

    def collision_test(self, rect):  # check if there is collison
        if self.rect.colliderect(rect.rect):
            return True

    def animation(self):  # contains animation for sprinting left/right idle left/right a
        if self.walk_count < 6:  # prevents index error

            self.walk_count += 1
        else:
            self.walk_count = 0  # resets index
        if self.right:  # if right key pressed
            self.image = self.walk_right_animation[self.walk_count]
            self.sprite_direction = True  # sprite direction is right

        elif self.left:  # if left key pressed
            self.image = self.walk_left_animation[self.walk_count]
            self.sprite_direction = False  # sprite direction is left

        else:
            if self.sprite_direction:  # sprite direction right
                self.image = self.idle_animation[self.walk_count]
            elif not self.sprite_direction:  # sprite direction left
                self.image = self.idle_animation_left[self.walk_count]

    def game_control(self):

        # player inputs
        user_input = pygame.key.get_pressed()

        if user_input[pygame.K_LEFT] and not (self.rect.colliderect(screen_border.left_height)) :
        # not crossing screen collision rect
            self.rect.x -= self.vel
            self.left = True
            self.right = False

        elif user_input[pygame.K_RIGHT] and not (
                self.rect.colliderect(screen_border.right_height)) :  # not crossing screen collision rect
            self.rect.x += self.vel
            self.left = False
            self.right = True
            ##
            if player.left_obsctacle_collision:
                player.vel *= -1
        else:
            self.left = False
            self.right = False

        if not self.is_jump:  # jump mechanics

            if user_input[pygame.K_SPACE]:  # breaking  not condition and executing next block
                self.is_jump = True
        else:
            # jump animation

            if self.jump_count >= -10 :  # jump will be in parabola shape (negative quadratic graph)
                if self.sprite_direction:  # jump facing right
                    if 10 >= self.jump_count > 1:
                        self.image = self.jump_animation_right[0]  # jump rise animation

                    elif 1 >= self.jump_count > -7:
                        self.image = self.jump_animation_right[1]  # mid jump animation

                    else:
                        self.image = self.jump_animation_right[2]  # jump land animation

                    neg = 1
                    if self.jump_count < 0 :  # creates turning point of negative quadratic graph
                        neg = -1

                    #if abs()
                    self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                    self.jump_count -= 1

                elif not self.sprite_direction:  # jump facing left
                    if 10 >= self.jump_count > 1:
                        self.image = self.jump_animation_left[0]

                    elif 1 >= self.jump_count > -7:
                        self.image = self.jump_animation_left[1]

                    else:
                        self.image = self.jump_animation_left[2]

                    neg = 1
                    if self.jump_count < 0 :  # creates turning point of negative quadratic graph
                        neg = -1
                    self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                    self.jump_count -= 1

            else:  # stops jump
                self.is_jump = False
                self.jump_count = 10

            if player.rect.y < 400:
                player.rect.y +=1

    def update(self):  # updates sprite
        self.animation()
        self.game_control()

pg = pygame.transform.scale(pygame.image.load(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\pixel_star_2.png'), (screen_width,screen_height))
# redraws screen
def redraw():
    clock.tick(20)
    screen.blit(pg,(0,0))
    background.run_background()
    #player.display_hit_box()
    obstacle_sprite.draw(screen)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.draw.rect(screen, (255, 255, 255) , obstacle, 2)


    pygame.display.update()




background = Background()

# bg = pygame.transform.scale(bg_temp, (screen_height, screen_width))
player = Player()
# sprite Class
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


obstacles_rect = obstacle_sprite.sprites()
obstacle= obstacles_rect[0]

player.rect.bottom += 1

# game loop
run = True
while run:

    redraw()
    collision_tolerance = 10

    if player.rect.colliderect(obstacle):
        if abs(obstacle.rect.bottom - player.rect.top) < collision_tolerance:
            pass

    if player.rect.colliderect(obstacle):
        if abs(obstacle.rect.right - player.rect.left) < collision_tolerance:
            player.rect.x = obstacle.rect.x+64


    if player.rect.colliderect(obstacle):
        if abs(obstacle.rect.left - player.rect.right) < collision_tolerance:
            player.rect.x = obstacle.rect.left - player.rect.w



    # player.vel *=-1

    # obstacle_collision = pygame.sprite.spritecollide(player, obstacle_sprite, False)
    # if obstacle_collision:
    #     if player.left:  # if left key pressed
    #         player.left_obsctacle_collision = True

    #     elif player.right:
    #         player.right_obsctacle_collision = True

    # if player.is_jump:

    #     if obstacle_collision:
    #         player.jump_obstacle_collision = True



    # elif not  obstacle_collision:
    #     player.left_obsctacle_collision = False
    #     player.right_obsctacle_collision = False
    #     player.jump_obstacle_collision = False




    def update(self):
        for bound in self.bound_list:
            if player.rect.colliderect(bound):
                self.obsctacle_collision = True
                break
            else:
                self.obsctacle_collision = False
        print(123)





    quit_game()