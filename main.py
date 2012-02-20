import math
import random

import pygame

# define the size of the screen
SCREENRECT = pygame.Rect(0, 0, 800, 600)

def main():
    """The main function which contains the game loop."""
    # initialize the pygame module
    pygame.init()
    # set the caption
    pygame.display.set_caption("missle command")
    # create a surface on screen
    screen = pygame.display.set_mode(SCREENRECT.size)
    # hide the mouse cursor
    pygame.mouse.set_visible(False)
    
    # setup the game clock
    clock = pygame.time.Clock()
    # define a variable to control the main loop
    running = True

    # create the missiles
    missiles = create_missiles()

    # create a sprite group to store the missiles
    missile_group = pygame.sprite.Group()
    missile_group.add(missiles)
    # create a sprite group to store other sprites
    sprites = pygame.sprite.Group()
    sprites.add(Crosshairs())
    # create a sprite group for the defense targets
    defense_targets = pygame.sprite.Group()

    # create and draw the background
    background = pygame.Surface(SCREENRECT.size)
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # main loop
    while running:
        # check for collisions between missiles and defense targets
        running = check_collisions(missile_group, defense_targets)

        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # check for game exit
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                launch_patriot(event.pos, defense_targets)


        # update the sprites
        missile_group.update()
        missile_group.clear(screen, background)
        missile_group.draw(screen)

        # update the sprites
        sprites.update()
        sprites.clear(screen, background)
        sprites.draw(screen)
        
        defense_targets.update()
        defense_targets.draw(screen)

        # update the display
        pygame.display.update()

        # maintain the frame rate
        clock.tick(30)

def create_missiles():
    """Creates a bunch of missiles."""
    missiles = []

    # get the width and height of the screen
    screen_width = SCREENRECT.width
    screen_height = SCREENRECT.height

    # a variety of colours for the missiles
    colours = [(255, 0, 0),
               (0, 255, 0),
               (0, 0, 255),
               (255, 255, 0),
               (0, 255, 255)]

    for i in range(0, 5):
        # generate a start and end coordinate with a
        # random x-axis value
        start = (random.randint(0, screen_width), 0)
        end = (random.randint(0, screen_width), screen_height)

        # calculate the distance between the two points on
        # both the x and y axis
        x = end[0] - start[0]
        y = end[1] - start[1]

        # calculate the angle required for the missile to
        # travel from the start coordinate to the end coordinate
        angle = math.atan(x / float(y))

        # get a random speed for the missile
        speed = random.randint(2, 5)

        # create the missile and add to the list
        missiles.append(Missile([start[0], start[1]], (angle, speed), colours[i]))
    
        print "Missle leaving (%s,%s), travelling to (%s, %s) " \
              "at an angle of %s and speed of %s" % \
              (start[0], start[1], end[0], end[1], angle, speed)

    return missiles

def launch_patriot(position, defense_group):
    """Launches a defense missile at a given target position."""
    # draw the target
    target = Target(position)
    defense_group.add(target)

def check_collisions(missile_group, defense_targets):
    """Checks if enemy missiles have collided with the defense targets
    or if any have reached the bottom of the screen."""
    # test for missile collisions with the defense targets 
    for dt in defense_targets:
        pygame.sprite.spritecollide(dt, missile_group, True)

    # test for missiles which have reached the bottom of the screen
    for m in missile_group:
        if m.position[1] >= SCREENRECT.height:
            return False

    return True

class Missile(pygame.sprite.Sprite):
    """Describes a missile."""
    
    def __init__(self, initial_position, vector, colour):
        """Initialises a new instance of missile."""
        pygame.sprite.Sprite.__init__(self)

        # draw the missile
        self.image = pygame.Surface([2, 2])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        # set the initial position of the missile
        self.position = initial_position
        # set the vector (angle and speed)
        self.vector = vector

    def update(self):
        """Updates the missile's position."""
        # calculate the new position of the missile
        self.position = self.get_new_position()
        # move the rectangle of the missile
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]

    def get_new_position(self):
        """Determines the missile's next position, based on its angle
        and speed."""
        # extract the angle and speed components from the vector
        (angle, z) = self.vector
        # determine the direction of travel and calculate dx and dy
        # accordingly
        (dx, dy) = (z * math.sin(angle), z * math.cos(angle))
        return [self.position[0] + dx, self.position[1] + dy]
 
class Crosshairs(pygame.sprite.Sprite):
    """The crosshairs used to target and destroy missiles."""
    def __init__(self):
        """Initialises a new instance of missile."""
        pygame.sprite.Sprite.__init__(self)
        
        # create a surface for the crosshair
        self.image = pygame.Surface([7, 7])
        # draw the crosshair
        pygame.draw.line(self.image, (255, 255, 255), [3, 0], [3, 7])
        pygame.draw.line(self.image, (255, 255, 255), [0, 3], [7, 3])
        # get the rectangle of the crosshair
        self.rect = self.image.get_rect(center=SCREENRECT.center)

    def update(self):
        """Updates the position of the crosshair."""
        self.rect.center = pygame.mouse.get_pos()

class Target(pygame.sprite.Sprite):
    """A target used to destroy enemy missiles."""
    def __init__(self, position):
        """Initialises a new instance of target."""
        pygame.sprite.Sprite.__init__(self)

        # set the image and rectangle of the defense target
        self.image = pygame.Surface([10, 10])
        self.image.fill((155, 155, 155))
        self.rect = self.image.get_rect(center=position)

# kick off the game by running the main function
if __name__=="__main__":
    main()
