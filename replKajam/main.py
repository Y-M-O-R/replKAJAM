import sys
import os.path
import pygame

pygame.init()

# screen
screen_width, screen_height = 960, 640
screen = pygame.display.set_mode((screen_width, screen_height))


class Boundary:
    def __init__(self, bound_screen):
        self.screen = bound_screen.get_rect()
        self.left_height = pygame.Rect((0, 0, 1, self.screen.height))
        self.top_width = pygame.Rect((0, 0, self.screen.width, 1))
        self.right_height = pygame.Rect((self.screen.width - 1, 0, 1, self.screen.height))
        self.bottom_width = pygame.Rect((0, self.screen.height - 1, self.screen.width, 1))
        self.bound_list = [self.left_height, self.top_width, self.right_height, self.bottom_width]


screen_border = Boundary(screen)


def quit():
    for event in pygame.event.get():  # loop to quit game

        if event.type == pygame.QUIT:  # fix this
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def redraw():
    pygame.display.update()


# player class contains everything player related
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
        self.file_location = os.path.join('img', 'pixel_platformer_player')

        # animation for sprite
        self.walk_right_animation = [pygame.image.load(os.path.join(self.file_location, 'run', '1.png')),
                                     pygame.image.load(os.path.join(self.file_location, 'run', '2.png')),
                                     pygame.image.load(os.path.join(self.file_location, 'run', '3.png')),
                                     pygame.image.load(os.path.join(self.file_location, 'run', '4.png')),
                                     pygame.image.load(os.path.join(self.file_location, 'run', '5.png')),
                                     pygame.image.load(os.path.join(self.file_location, 'run', '6.png')),
                                     pygame.image.load(os.path.join(self.file_location, 'run', '7.png'))
                                     ]

        self.walk_left_animation = []

        for image in self.walk_right_animation:
            self.walk_left_animation.append(pygame.transform.flip(image, True, False))

        self.jump_animation_right = [pygame.image.load(os.path.join(self.file_location, 'jump', '1.png')),
                                     pygame.image.load(os.path.join(self.file_location, 'jump', '2.png')),
                                     pygame.image.load(os.path.join(self.file_location, 'jump', '3.png'))
                                     ]
        self.jump_animation_left = []

        for image in self.jump_animation_right:
            self.jump_animation_left.append(pygame.transform.flip(image, True, False))
        self.idle_animation = [
            pygame.image.load(os.path.join(self.file_location, 'idle', '1.png')),
            pygame.image.load(os.path.join(self.file_location, 'idle', '2.png')),
            pygame.image.load(os.path.join(self.file_location, 'idle', '3.png')),
            pygame.image.load(os.path.join(self.file_location, 'idle', '4.png')),
            pygame.image.load(os.path.join(self.file_location, 'idle', '5.png')),
            pygame.image.load(os.path.join(self.file_location, 'idle', '6.png')),
            pygame.image.load(os.path.join(self.file_location, 'idle', '7.png'))
        ]
        self.idle_animation_left = []

        for image in self.idle_animation:
            self.idle_animation_left.append(pygame.transform.flip(image, True, False))

        self.walk_count = 0
        self.image = self.idle_animation[self.walk_count]

        self.rect = self.image.get_rect()
        # self.rect.width, self.rect.height = width, height
        self.rect.midbottom = (screen_width // 2, screen_height)
        self.sprite_direction = True

    def check_health(self):
        if self.health <= 0:
            return True
        return False

    def display_hit_box(self):  # displays object hit box used for testing
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

        if user_input[pygame.K_LEFT] and not (
                self.rect.colliderect(screen_border.left_height)):  # not crossing screen collision rect
            self.rect.x -= self.vel
            self.left = True
            self.right = False

        elif user_input[pygame.K_RIGHT] and not (
                self.rect.colliderect(screen_border.right_height)):  # not crossing screen collision rect
            self.rect.x += self.vel
            self.left = False
            self.right = True
        else:
            self.left = False
            self.right = False

        if not self.is_jump:  # jump mechanics

            if user_input[pygame.K_SPACE]:  # breaking  not condition and executing next block
                self.is_jump = True
        else:
            # jump animation
            if self.jump_count >= -10:  # jump will be in parabola shape (negative quadratic graph)
                if self.sprite_direction:  # jump facing right
                    if 10 >= self.jump_count > 1:
                        self.image = self.jump_animation_right[0]  # jump rise animation

                    elif 1 >= self.jump_count > -7:
                        self.image = self.jump_animation_right[1]  # mid jump animation

                    else:
                        self.image = self.jump_animation_right[2]  # jump land animation

                    neg = 1
                    if self.jump_count < 0:  # creates turning point of negative quadratic graph
                        neg = -1
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
                    if self.jump_count < 0:  # creates turning point of negative quadratic graph
                        neg = -1
                    self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                    self.jump_count -= 1

            else:  # stops jump
                self.is_jump = False
                self.jump_count = 10

    def update(self):  # updates sprite
        self.animation()
        self.game_control()


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
run = True
while run:
    all_sprites.draw(screen)
    all_sprites.update()
    redraw()
    quit()
