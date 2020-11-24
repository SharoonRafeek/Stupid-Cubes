import pygame
import random

# variables
particles = []
velocity = 10
width = 800
height = 600
game_start = True

# initialising pygame and screen
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stupid Cubes!")

# fps
clock = pygame.time.Clock()
fps = 15

# color object
class Color:
    def __init__(self):
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.pink = (255, 192, 200)
        self.brown = (165, 42, 42)
        self.violet = (127, 0, 255)
        self.orange = (255, 165,0)
        self.gold = (255, 215, 0)


# player object
class Player:
    def __init__(self, x, y, color, vel_x, vel_y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.block_size = 20
        self.color = color


    # boundary of the player object
    def boundary(self):
        if self.x <= 0:
            self.vel_x = 10
            self.vel_y = 0
        elif self.x >= width - self.block_size:
            self.vel_x = -10
            self.vel_y = 0
        if self.y <= 60: 
            self.vel_y = 10
            self.vel_x = 0
        elif self.y >= height - self.block_size:
            self.vel_y = -10
            self.vel_x = 0


    # drawing player on screen
    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.block_size, self.block_size)
        pygame.draw.rect(screen, self.color, rect)


    # collision of smaller cubes and player cubes
    def collision(self):
        size = 6
        for particle in particles:
            particle_x = particle[1][0]
            particle_y = particle[1][1]
            if particle_x > self.x + self.block_size and particle_x < self.x or particle_x + size > self.x and particle_x + size < self.x + self.block_size:
                if particle_y > self.y + self.block_size and particle_y < self.y or particle_y + size > self.y and particle_y + size < self.y + self.block_size:
                    x = particles.index(particle)
                    del particles[x]
                    return True


# small cubes
def eatables():
    for i in range(100):
        x = round(random.randint(30, width - 30) / 10) * 10
        y = round(random.randint(80, height - 30) / 10) * 10
        color = random.choice(colors_list)
        size = 6
        particle_rect = (x, y, size, size)
        particle = [color, particle_rect]
        particles.append(particle)


# drawing small cubes
def drawing_eatables():
    for particle in particles:
        pygame.draw.rect(screen, particle[0], particle[1])


# text on screen
def message(msg, color, x, y, font, size):
    font = pygame.font.SysFont(font, size)
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, (x, y))


# drawing lines
def drawing_lines(color, point1, point2):
    pygame.draw.line(screen, color, point1, point2)


# initialising colors
color = Color()
colors_list = [color.red, color.blue, color.white, color.green, color.yellow, color.pink, color.brown, color.violet, color.orange, color.gold]


# main function
def main():
    global particles, game_start

    # initialising 2 player object and eatables
    karlson = Player(width - (width - 170), height // 2, color.red, velocity, velocity)
    billy = Player(width - 170, height // 2, color.blue, velocity, velocity)
    count_billy, count_karlson = 0, 0
    eatables()

    # starting and stoping triggers
    run = True
    game_over = False

    # main loop
    while run:

        screen.fill(color.black)
        karlson.boundary()
        billy.boundary()
        karlson.draw()
        billy.draw()
        drawing_eatables()

        message(f"RED : {str(count_karlson)}", color.white, 20, 20, "Consolas", 30)
        message(f"BLUE : {str(count_billy)}", color.white, width - 175, 20, "Consolas", 30)

        drawing_lines(color.white, (0, 60), (width, 60))

        # menu loop
        while game_start:
            screen.fill(color.black)
            message("CLICK TO START", color.white, width/2 - 200, height/2 - 20, "Orator Std", 50)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_start = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        game_start = False
                if event.type == pygame.MOUSEBUTTONUP:
                    game_start = False

        # game over loop
        while game_over:
            screen.fill(color.black)
            message("GAME OVER!", color.white, width/2 - 125, height/2 - 40, "Orator Std", 50)
            if count_billy > count_karlson:
                message("Blue Won!", color.blue, width/2 - 110, height/2 + 30, "Orator Std", 50)
            elif count_billy == count_karlson:
                message("TiE!", color.white, width/2 - 40, height/2 + 30, "Orator Std", 50)
            else:
                message("Red Won!", color.red, width/2 - 95, height/2 + 30, "Orator Std", 50)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_over = False
                if event.type == pygame.MOUSEBUTTONUP:
                    particles = []
                    game_over = False
                    run = False
                    game_start = False
                    main()
                        

        # player movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    karlson.vel_x = velocity
                    karlson.vel_y = 0
                elif event.key == pygame.K_LEFT:
                    karlson.vel_x = -velocity
                    karlson.vel_y = 0
                elif event.key == pygame.K_DOWN:
                    karlson.vel_y = velocity
                    karlson.vel_x = 0
                elif event.key == pygame.K_UP:
                    karlson.vel_y = -velocity
                    karlson.vel_x = 0
                
                if event.key == pygame.K_d:
                    billy.vel_x = velocity
                    billy.vel_y = 0
                elif event.key == pygame.K_a:
                    billy.vel_x = -velocity
                    billy.vel_y = 0
                elif event.key == pygame.K_s:
                    billy.vel_y = velocity
                    billy.vel_x = 0
                elif event.key == pygame.K_w:
                    billy.vel_y = -velocity
                    billy.vel_x = 0        

        billy.x += billy.vel_x
        billy.y += billy.vel_y
        karlson.x += karlson.vel_x
        karlson.y += karlson.vel_y

        # size increasing
        if billy.collision():
            billy.block_size += 1
            count_billy += 1
        if karlson.collision():
            karlson.block_size += 1
            count_karlson += 1

        # triggering game over
        if count_billy + count_karlson == 100:
            game_over = True

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
