import pygame

pygame.init()
screen = pygame.display.set_mode((960, 640))

clock = pygame.time.Clock()


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
        # a = screen.blit(image, (0, 0))
        image = pygame.transform.scale(image, (200, 200))

        # Assuming black works as the transparent color
        ##image.set_colorkey((0, 0, 0))
        transColor = image.get_at((0, 0))
        image.set_colorkey(transColor)

        # Return the image
        return image  # , a


ss = SpriteSheet(r'C:\Users\ryous\OneDrive\Documents\GitHub\replKAJAM\replKajam\img\background\earth.png')
ls = []
b = 0
c = 0
n = 9

for i in range(70):
    ls.append(ss.get_image(b, c, 99, 99))
    b += 99
    if i >= n:
        c += 99
        n += 9
        b = 0

bcb = 0
run = True
while run:

    if bcb == 69:
        bcb = 0

    screen.blit(ls[bcb], (200, 200))
    pygame.display.update()
    bcb += 1
    clock.tick(40)
    for event in pygame.event.get():  # loop to quit game
        if event.type == pygame.QUIT:  # fix this
            pygame.quit()
