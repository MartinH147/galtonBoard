# credit to https://www.youtube.com/watch?v=-q_Vje2a6eY

# Import relevant modules
import pygame as pg
from random import randrange
import pymunk.pygame_util

# Sets the plane of the window
pymunk.pygame_util.positive_y_is_up = False

# Variables for window dimensions and frames per second
RES = WIDTH, HEIGHT = 600, 750
FPS = 60

# Variables for general pygame functionality
pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

# General variables
space = pymunk.Space()
space.gravity = 0, 8000
ball_mass, ball_radius = 1, 7
segment_thickness = 6

# Variables for interface dimensions. Refer to galton board schematic
a, b, c, d = 0, 50, 18, 20
x1, x2, x3, x4 = a, WIDTH // 2 - c, WIDTH // 2 + c, WIDTH
y1, y2, y3, y4, y5 = b, HEIGHT // 4 - d, HEIGHT // 4, HEIGHT // 2 - 2 * b, HEIGHT - 4 * b
L1, L2, L3, L4 = (x1, -100), (x1, y1), (x2, y2), (x2, y3)
R1, R2, R3, R4 = (x4, -100), (x4, y1), (x3, y2), (x3, y3)
B1, B2 = (0, HEIGHT), (WIDTH, HEIGHT)


# Create a ball object
def create_ball(space):
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = randrange(x1, x4), randrange(-y1, y1)
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.1
    ball_shape.friction = 0.1
    space.add(ball_body, ball_shape)
    return ball_body


# Create a segment object
def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pg.color.THECOLORS[color]
    space.add(segment_shape)


# Create a pin object
def create_pin(x, y, space, color):
    circle_shape = pymunk.Circle(space.static_body, radius=10, offset=(x, y))
    circle_shape.color = pg.color.THECOLORS[color]
    circle_shape.elasticity = 0.1
    circle_shape.friction = 0.5
    space.add(circle_shape)


# Two loops are used to generate elements at regular intervals to each other, with rows offset
pin_y, step = y4, 60
for i in range(7):
    pin_x = -1.5 * step if i % 2 else -step
    for j in range(WIDTH // step + 2):
        # Generate pins
        create_pin(pin_x, pin_y, space, 'darkgoldenrod')
        if i == 6:
            # Generates the collection segments
            create_segment((pin_x, pin_y + 30), (pin_x, HEIGHT), segment_thickness, space, 'saddlebrown')
        pin_x += step
    pin_y += 0.5 * step

# Generate the funnel
platforms = (L1, L2), (L2, L3), (L3, L4), (R1, R2), (R2, R3), (R3, R4)
for platform in platforms:
    create_segment(*platform, segment_thickness, space, 'saddlebrown')

# Generate the floor segment
create_segment(B1, B2, segment_thickness, space, 'saddlebrown')

# An array containing all 300 ball objects
balls = [('mediumaquamarine', create_ball(space)) for j in range(500)]

# Loop for the programs run time
while True:
    # Set background colour
    surface.fill(pg.Color('lightgoldenrodyellow'))

    # Event handler
    # If the program is quit then terminate itself
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()

    # Generate the space, at each clock tick
    space.step(1 / FPS)
    space.debug_draw(draw_options)

    # Generate the balls
    [pg.draw.circle(surface, color, (int(ball.position[0]), int(ball.position[1])), ball_radius) for color, ball in balls]

    # Updates the display with the clock tick (set at 60FPS)
    pg.display.flip()
    clock.tick(FPS)
