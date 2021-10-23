import os
import random
import sys

import pygame

screen_width, screen_height = 1000, 700
pygame.init()
pygame.display.set_caption('Level Editor')
myfont = pygame.font.SysFont('Comic Sans MS', 30)
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


class LevelEditor:
    def __init__(self):

        self.sprite_list = [
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
        self.sprite_list_rect = []

        self.sprite_menu_height = screen_height // self.sprite_list[
            0].get_height()  # remainder 8 # check amount of sprites that can fit in column
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_rect = pygame.Rect(self.mouse_x, self.mouse_y, 5, 5)

        self.mouse_click = False
        self.clicked_sprite = False

    def get_mouse_pos(self): # get mouse positon
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_rect = pygame.Rect(self.mouse_x, self.mouse_y, 5, 5)

    def get_sprite_rect(self):  # creates the rects for sprite_list
        y_column = 0
        for sprite_block in range(self.sprite_menu_height):
            if sprite_block < len(self.sprite_list):
                block_x, block_y, block_width, block_height = self.sprite_list[sprite_block].get_rect()
                self.sprite_list[sprite_block].get_rect().y += block_height  # add new height
                self.sprite_list_rect.append([block_x, y_column, block_width, block_height])
                y_column += block_height

    def sprite_menu(self):  # displays sprites
        for (image, image_rect) in zip(self.sprite_list, self.sprite_list_rect):
            screen.blit(image, image_rect)
            pygame.draw.rect(screen, (0, 0, 0), image_rect, 2)

    def sprite_clicked(self):  # checks if mouse interacts with sprite_menu
        if self.mouse_click:
            for img_rect in self.sprite_list_rect:
                if self.mouse_rect.colliderect(img_rect):
                    self.mouse_sprite_collide = img_rect
                    self.clicked_sprite = True

    def sprite_place(self):  # allows sprite to be placed with rect argument
        if self.clicked_sprite:
            pygame.draw.rect(screen, (255, 200, 0), self.mouse_sprite_collide, 3)
        pygame.display.update()

    def sprite_edit(self):  # allows for sprites to be edited
        pass

    def level_save(self):  # saves level built
        pass


def game_event():
    for event in pygame.event.get():  # loop to quit game
        level.mouse_click = False
        # level.mouse_click = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                level.mouse_click = True
                level.get_mouse_pos()

                # sprite_menu.mouse_x, sprite_menu.mouse_y = mx, my
        if event.type == pygame.QUIT:  # fix this
            pygame.quit()

            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def redraw():
    level.sprite_menu()
    pygame.display.update()


mx, my = pygame.mouse.get_pos()
level = LevelEditor()
screen.fill((220, 220, 220))
level.get_sprite_rect()
run = True
while run:
    level.sprite_clicked()
    level.sprite_place()
    clock.tick(20)
    game_event()

    redraw()
