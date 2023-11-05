import pygame
from board import boards
import math
import copy

pygame.init()

# Width and Height values for the screen
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])   # Setting the features of the screen
timer = pygame.time.Clock()
fps = 60    # Maximum fps limit for the game
font = pygame.font.Font(size=30)
level = copy.deepcopy(boards)  # You can use that code when you add new levels to the game (boards[0] or boards[1] could be different levels)
color = "blue"
PI = math.pi

# The code that loads and scales all of the pacman images to the list
pacman_imgs = []
for i in range(1,5):
    pacman_imgs.append(pygame.transform.scale(pygame.image.load(f"images/pacman_images/{i}.png"), (45,45)))

# Fetching the ghosts images
blinky_img = pygame.transform.scale(pygame.image.load(f"images/ghosts_images/red.png"), (45,45))
pinky_img = pygame.transform.scale(pygame.image.load(f"images/ghosts_images/pink.png"), (45,45))
inky_img = pygame.transform.scale(pygame.image.load(f"images/ghosts_images/blue.png"), (45,45))
clyde_img = pygame.transform.scale(pygame.image.load(f"images/ghosts_images/orange.png"), (45,45))
spooked_img = pygame.transform.scale(pygame.image.load(f"images/ghosts_images/powerup.png"), (45,45))
dead_img = pygame.transform.scale(pygame.image.load(f"images/ghosts_images/dead.png"), (45,45))

# Starting point's coordinates of the pacman
pacman_x = 450
pacman_y = 663
direction = 0   # Initial direction of the pacman

# Setting up ghosts coordinates
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 440
clyde_y = 438
clyde_direction = 2

counter = 0     # A variable to change pacman's asset
turns_allowed = [False, False, False, False]    # Checks can pacman turn to r,l,u,d respectively
direction_command = 0
pacman_speed = 2

score = 0
powerup = False
power_counter = 0

eaten_ghost = [False, False, False, False]
targets = [(pacman_x, pacman_y), (pacman_x, pacman_y), (pacman_x, pacman_y), (pacman_x, pacman_y)]  # Target positions of the each ghosts
blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False
# Variable to keep track on is the ghost in the starting box
blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False
moving = False  # Variable to set ghosts' moving
ghost_speeds = [2, 2, 2, 2]
start_counter = 0
lives = 3

game_over = False
game_won = False

def draw_board(level):
    num1 = ((HEIGHT - 50) // 32)    # Height of the each little cell
    num2 = (WIDTH // 30)    # Width of the each little cell

    # Iterating every single row and column
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:     # Drawing white dots on the screen
                pygame.draw.circle(screen,
                                   "white",
                                   (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)),  # (0.5 * num2) is placing the dot to the middle of the each cell
                                   4)   # Setting size of the dot
                # Second parameter of the function is the x and y coordinates of the dot that we want to draw
            if level[i][j] == 2:     # Drawing white big dots on the screen
                pygame.draw.circle(screen,
                                   "white",
                                   (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)),
                                   10)   # Setting size of the dot
                # Second parameter of the function is the x and y coordinates of the dot that we want to draw
            if level[i][j] == 3:
                pygame.draw.line(screen,
                                 color,
                                 (j * num2 + (0.5 * num2), i * num1),   # Starting point of the line in the each cell
                                 (j * num2 + (0.5 * num2), i * num1 + num1), # Ending point of the line in the each cell
                                 3)
            if level[i][j] == 4:
                pygame.draw.line(screen,
                                 color,
                                 (j * num2, i * num1 + (0.5 * num1)),   # Starting point of the line in the each cell
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), # Ending point of the line in the each cell
                                 3)
            if level[i][j] == 5:  # Creating one of the corners
                pygame.draw.arc(screen,
                                color,
                                [(j * num2 - (0.5 * num2)), (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI/2,    # Setting the curve using angles (from 0 to 90)
                                3)
            if level[i][j] == 6:
                pygame.draw.arc(screen,
                                color,
                                [(j * num2 + (0.5 * num2)), (i * num1 + (0.5 * num1)), num2, num1],
                                PI/2, PI,    # Setting the curve using angles (from 90 to 180)
                                3)
            if level[i][j] == 7:
                pygame.draw.arc(screen,
                                color,
                                [(j * num2 + (0.5 * num2)), (i * num1 - (0.5 * num1)), num2, num1],
                                PI, 3*PI/2,    # Setting the curve using angles (from 0 to 90)
                                3)
            if level[i][j] == 8:
                pygame.draw.arc(screen,
                                color,
                                [(j * num2 - (0.5 * num2)), (i * num1 - (0.5 * num1)), num2, num1],
                                3*PI/2, 0,    # Setting the curve using angles (from 90 to 180)
                                3)
            if level[i][j] == 9:
                pygame.draw.line(screen,
                                 "white",
                                 (j * num2, i * num1 + (0.5 * num1)),   # Starting point of the line in the each cell
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), # Ending point of the line in the each cell
                                 3)

def draw_player():
    if direction == 0:    # Right
        screen.blit(pacman_imgs[counter // 5], (pacman_x, pacman_y))
    elif direction == 1:  # Left
        screen.blit(pygame.transform.flip(pacman_imgs[counter // 5], True, False), (pacman_x, pacman_y))   # Flip's second param is flipping on x axis, third is flipping on y axis
    elif direction == 2:  # Up
        screen.blit(pygame.transform.rotate(pacman_imgs[counter // 5], 90), (pacman_x, pacman_y))  # Instead of flipping, rotate the image by 90 degrees
    elif direction == 3:  # Down
        screen.blit(pygame.transform.rotate(pacman_imgs[counter // 5], -90), (pacman_x, pacman_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    num3 = 15
    # Check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:  # Check is the pacman within the game's limit
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_pacman(pac_x, pac_y):
    # If there is no wall then the pacman will move
    if direction == 0 and turns_allowed[0]:
        pac_x += pacman_speed
    elif direction == 1 and turns_allowed[1]:
        pac_x -= pacman_speed
    if direction == 2 and turns_allowed[2]:
        pac_y -= pacman_speed
    elif direction == 3 and turns_allowed[3]:
        pac_y += pacman_speed
    return pac_x, pac_y

def check_collision(score, power, power_count, eaten_ghosts):
    # The function that checks eating something
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < pacman_x < 870:
        if level[center_y // num1][center_x // num2] == 1:  # Checks is pacman in the cell that includes a little dot
            level[center_y // num1][center_x // num2] = 0
            score += 10
        if level[center_y // num1][center_x // num2] == 2:  # Checks is pacman in the cell that includes a big dot
            level[center_y // num1][center_x // num2] = 0
            score += 50

            # Powerup codes
            power = True
            power_count = 0     # Variable to counter for the powerup (resetting timer in every powerup)
            eaten_ghosts = [False, False, False, False]
    return score, power, power_count, eaten_ghosts

def draw_misc():
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (10, 920))  # Placing the score on the screen
    if powerup:
        pygame.draw.circle(screen, "blue", (870, 930), 15)      # The circle will shown when pacman powerup
    for i in range(lives):
        screen.blit(pygame.transform.scale(pacman_imgs[0], (30, 30)), (400 + i * 40, 915))  # The last parameter is positioning the lives symbol

    if game_over:
        pygame.draw.rect(screen, "white", [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, "dark gray", [70, 220, 760, 260], 0, 10)
        gameover_text = font.render("Game over! Space bar to restart!", True, "red")
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, "white", [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, "dark gray", [70, 220, 760, 260], 0, 10)
        victory_text = font.render("Victory! Space bar to restart!", True, "green")
        screen.blit(victory_text, (100, 300))

class Ghost:
    def __init__(self, x_coor, y_coor, target, speed, img, direct, dead, box, id):
        self.x_coord = x_coor
        self.y_coord = y_coor
        self.center_x = self.x_coord + 22
        self.center_y = self.y_coord + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direct = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()    # Hit box of each ghost

    def draw(self):
        # The statement that determines the shape of the ghost
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_coord, self.y_coord))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_coord, self.y_coord))
        else:
            screen.blit(dead_img, (self.x_coord, self.y_coord))

        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))   # Determining the hitbox of the ghost
        return ghost_rect

    def check_collisions(self):
        num1 = (HEIGHT - 50) // 32
        num2 = WIDTH // 30
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            # The statements that checks the inside of the cell (anything, little dot, big dot) and more
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direct == 2 or self.direct == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direct == 0 or self.direct == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and
                            (self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and
                            (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and
                            (self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and
                            (self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True

        # Check is the ghost in the box or not
        if 350 < self.x_coord < 550 and 370 < self.y_coord < 480:
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box

    def move_clyde(self):
        # Clyde is going to turn whenever advantageous for pursuit
        if self.direct == 0:
            if self.target[0] > self.x_coord and self.turns[0]:
                self.x_coord += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                if self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                else:
                    self.x_coord += self.speed
        elif self.direct == 1:
            if self.target[1] > self.y_coord and self.turns[3]:
                self.direct = 3
            elif self.target[0] < self.x_coord and self.turns[1]:
                self.x_coord -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                if self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                else:
                    self.x_coord -= self.speed
        elif self.direct == 2:
            if self.target[0] < self.x_coord and self.turns[1]:
                self.direct = 1
                self.x_coord -= self.speed
            elif self.target[1] < self.y_coord and self.turns[2]:
                self.direct = 2
                self.y_coord -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                else:
                    self.y_coord -= self.speed
        elif self.direct == 3:
            if self.target[1] > self.y_coord and self.turns[3]:
                self.y_coord += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                else:
                    self.y_coord += self.speed

        # The code for the portal in the game
        if self.x_coord < -30:
            self.x_coord = 900
        elif self.x_coord > 900:
            self.x_coord = 0

        return self.x_coord, self.y_coord, self.direct

    def move_blinky(self):
        # Blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direct == 0:
            if self.target[0] > self.x_coord and self.turns[0]:
                self.x_coord += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
            elif self.turns[0]:
                self.x_coord += self.speed
        elif self.direct == 1:
            if self.target[0] < self.x_coord and self.turns[1]:
                self.x_coord -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[1]:
                self.x_coord -= self.speed
        elif self.direct == 2:
            if self.target[1] < self.y_coord and self.turns[2]:
                self.direct = 2
                self.y_coord -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
            elif self.turns[2]:
                self.y_coord -= self.speed
        elif self.direct == 3:
            if self.target[1] > self.y_coord and self.turns[3]:
                self.y_coord += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
            elif self.turns[3]:
                self.y_coord += self.speed

        # The code for the portal in the game
        if self.x_coord < -30:
            self.x_coord = 900
        elif self.x_coord > 900:
            self.x_coord = 0

        return self.x_coord, self.y_coord, self.direct

    def move_inky(self):
        # Inky turns up or down at any point to pursue, but left and right only on collision
        if self.direct == 0:
            if self.target[0] > self.x_coord and self.turns[0]:
                self.x_coord += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                if self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                else:
                    self.x_coord += self.speed
        elif self.direct == 1:
            if self.target[1] > self.y_coord and self.turns[3]:
                self.direct = 3
            elif self.target[0] < self.x_coord and self.turns[1]:
                self.x_coord -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                if self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                else:
                    self.x_coord -= self.speed
        elif self.direct == 2:
            if self.target[1] < self.y_coord and self.turns[2]:
                self.direct = 2
                self.y_coord -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[2]:
                self.y_coord -= self.speed
        elif self.direct == 3:
            if self.target[1] > self.y_coord and self.turns[3]:
                self.y_coord += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[3]:
                self.y_coord += self.speed

        # The code for the portal in the game
        if self.x_coord < -30:
            self.x_coord = 900
        elif self.x_coord > 900:
            self.x_coord = 0

        return self.x_coord, self.y_coord, self.direct

    def move_pinky(self):
        # Pinky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direct == 0:
            if self.target[0] > self.x_coord and self.turns[0]:
                self.x_coord += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
            elif self.turns[0]:
                self.x_coord += self.speed
        elif self.direct == 1:
            if self.target[1] > self.y_coord and self.turns[3]:
                self.direct = 3
            elif self.target[0] < self.x_coord and self.turns[1]:
                self.x_coord -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[1]:
                self.x_coord -= self.speed
        elif self.direct == 2:
            if self.target[0] < self.x_coord and self.turns[1]:
                self.direct = 1
                self.x_coord -= self.speed
            elif self.target[1] < self.y_coord and self.turns[2]:
                self.direct = 2
                self.y_coord -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.target[1] > self.y_coord and self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_coord += self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                else:
                    self.y_coord -= self.speed
        elif self.direct == 3:
            if self.target[1] > self.y_coord and self.turns[3]:
                self.y_coord += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.target[1] < self.y_coord and self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_coord -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_coord and self.turns[0]:
                    self.direct = 0
                    self.x_coord += self.speed
                elif self.target[0] < self.x_coord and self.turns[1]:
                    self.direct = 1
                    self.x_coord -= self.speed
                else:
                    self.y_coord += self.speed

        # The code for the portal in the game
        if self.x_coord < -30:
            self.x_coord = 900
        elif self.x_coord > 900:
            self.x_coord = 0

        return self.x_coord, self.y_coord, self.direct

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    # That function rechanges ghosts' targets in the game

    # The statement determines the targets of ghosts while powerup
    if pacman_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if pacman_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)  # When the ghost eaten, the ghost will go to this coordinates

    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky_dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (pacman_x, pacman_y)
        else:
            blink_target = return_target

        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, pacman_y)
        elif not inky_dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (pacman_x, pacman_y)
        else:
            ink_target = return_target

        if not pinky.dead and not eaten_ghost[2]:
            pink_target = (pacman_x, runaway_y)
        elif not pinky_dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (pacman_x, pacman_y)
        else:
            pink_target = return_target

        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 460)
        elif not clyde_dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (pacman_x, pacman_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (pacman_x, pacman_y)
        else:
            blink_target = return_target

        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (pacman_x, pacman_y)
        else:
            ink_target = return_target

        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (pacman_x, pacman_y)
        else:
            pink_target = return_target

        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (pacman_x, pacman_y)
        else:
            clyd_target = return_target


    return [blink_target, ink_target, pink_target, clyd_target]     # Ghosts' targets

run = True
while run:
    # The code that process every iteration on the game
    timer.tick(fps)

    # The code that animates the pacman
    if counter < 19:
        counter += 1
    else:
        counter = 0

    # The statement for powerup
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]

    # The statement that controls moving after a while in the beginning of the game
    if start_counter < 180 and not game_over and not game_won:
        moving = False
        start_counter += 1
    else:
        moving = True

    screen.fill("black")    # Color of the screen
    draw_board(level)
    center_x = pacman_x + 23
    center_y = pacman_y + 24

    # Setting up the speeds of ghosts when they're dead and alive
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    # Win condition
    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    pacman_circle = pygame.draw.circle(screen, "black", (center_x, center_y), 20, 2)     # That code represents hitbox of the pacman
    draw_player()

    # Instantiating ghosts
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead, clyde_box, 3)

    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    turns_allowed = check_position(center_x, center_y)
    if moving:
        pacman_x, pacman_y = move_pacman(pacman_x, pacman_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        if not clyde_dead and not clyde.in_box:
            clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
        else:
            clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

    score, powerup, power_counter, eaten_ghost = check_collision(score, powerup, power_counter, eaten_ghost)

    # The statement that handles colliding with ghosts (eating, losing lives)
    if not powerup:
        if (pacman_circle.colliderect(blinky.rect) and not blinky.dead) or \
            (pacman_circle.colliderect(inky.rect) and not inky.dead) or \
             (pacman_circle.colliderect(pinky.rect) and not pinky.dead) or \
              (pacman_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:  # When pacman lose a live, that code will reset some variables
                lives -= 1
                start_counter = 0

                pacman_x = 450
                pacman_y = 663
                direction = 0
                direction_command = 0

                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2

                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False

                powerup = False
                power_counter = 0
            else:
                game_over = True
                moving = False
                start_counter = 0
    else:
        if pacman_circle.colliderect(blinky.rect) and not blinky.dead and eaten_ghost[0]:
            if lives > 0:  # When pacman lose a live, that code will reset some variables
                lives -= 1
                start_counter = 0

                pacman_x = 450
                pacman_y = 663
                direction = 0
                direction_command = 0

                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2

                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False

                powerup = False
                power_counter = 0
            else:
                game_over = True
                moving = False
                start_counter = 0
        if pacman_circle.colliderect(inky.rect) and not inky.dead and eaten_ghost[1]:
            if lives > 0:  # When pacman lose a live, that code will reset some variables
                lives -= 1
                start_counter = 0

                pacman_x = 450
                pacman_y = 663
                direction = 0
                direction_command = 0

                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2

                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False

                powerup = False
                power_counter = 0
            else:
                game_over = True
                moving = False
                start_counter = 0
        if pacman_circle.colliderect(pinky.rect) and not pinky.dead and eaten_ghost[2]:
            if lives > 0:  # When pacman lose a live, that code will reset some variables
                lives -= 1
                start_counter = 0

                pacman_x = 450
                pacman_y = 663
                direction = 0
                direction_command = 0

                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2

                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False

                powerup = False
                power_counter = 0
            else:
                game_over = True
                moving = False
                start_counter = 0
        if pacman_circle.colliderect(clyde.rect) and not clyde.dead and eaten_ghost[3]:
            if lives > 0:  # When pacman lose a live, that code will reset some variables
                lives -= 1
                start_counter = 0

                pacman_x = 450
                pacman_y = 663
                direction = 0
                direction_command = 0

                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2

                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False

                powerup = False
                power_counter = 0
            else:
                game_over = True
                moving = False
                start_counter = 0

        if pacman_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:  # Blinky's dead
            blinky_dead = True
            eaten_ghost[0] = True
            score += (2 ** eaten_ghost.count(True)) * 100   # Increase the score when blinky is eaten
        if pacman_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:  # Inky's dead
            inky_dead = True
            eaten_ghost[1] = True
            score += (2 ** eaten_ghost.count(True)) * 100   # Increase the score when inky is eaten
        if pacman_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:  # Pinky's dead
            pinky_dead = True
            eaten_ghost[2] = True
            score += (2 ** eaten_ghost.count(True)) * 100   # Increase the score when pinky is eaten
        if pacman_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:  # Clyde's dead
            clyde_dead = True
            eaten_ghost[3] = True
            score += (2 ** eaten_ghost.count(True)) * 100   # Increase the score when clyde is eaten


    for event in pygame.event.get():    # Looping all of the events that you do in the game (keyboard, mouse, buttons..)

        # The code that stops quits from the game
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:  # The control to perceive the touching any button on the keyboard
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                start_counter = 0

                pacman_x = 450
                pacman_y = 663
                direction = 0
                direction_command = 0

                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2

                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False

                powerup = False
                power_counter = 0
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:  # The control to perceive the stopping touching any button on the keyboard
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    # The code that turns the pacman to direction that whatever you want
    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i

    # The code that allows to the pacman use the teleportation from the left and right
    if pacman_x > 900:
        pacman_x = -47
    elif pacman_x < -50:
        pacman_x = 897

    # If the ghost eaten and returned the box successfully, then make the ghost as normal
    if blinky.in_box and blinky.dead:
        blinky_dead = False
    if inky.in_box and inky.dead:
        inky_dead = False
    if pinky.in_box and pinky.dead:
        pinky_dead = False
    if clyde.in_box and clyde.dead:
        clyde_dead = False

    pygame.display.flip()

pygame.quit()   # That code will process when the while loop is over
