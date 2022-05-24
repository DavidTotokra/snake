import time
from pygame.locals import*
import pygame
import random

# Size of the block
Size = 40
COLOR = (139,103,182)
pygame.display.set_caption('Snake eating')

class Food:
    def __init__(self, dad_screen):
        self.dad_screen = dad_screen
        self.image = pygame.image.load("food.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.x = Size*2
        self.y = Size*2

    def draw(self):
        self.dad_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,14)*Size
        self.y = random.randint(1,14)*Size


class Snake:
    def __init__(self, dad_screen):
        self.lenght = 1
        self.dad_screen = dad_screen
        self.block = pygame.image.load("block.jpg").convert()
        self.direction = 'down'
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_down(self):
        self.direction = 'down'

    def move_up(self):
        self.direction = 'up'

    def draw(self):
        self.dad_screen.fill(COLOR)
        for i in range(self.lenght):
            self.dad_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


    def walk(self):

        # update body
        for i in range(self.lenght-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= Size
        if self.direction == 'right':
            self.x[0] += Size
        if self.direction == 'down':
            self.y[0] += Size
        if self.direction == 'up':
            self.y[0] -= Size

        self.draw()


    def increase_lenght(self):
        self.lenght += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((950,600))
        # Color in the Background using rgb
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.food = Food(self.surface)
        self.food.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + Size:
            if y1 >= y2 and y1 < y2 + Size:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.lenght}",True,(200,200,200))
        self.surface.blit(score,(750,50))

    def show_game_over(self):
        self.surface.fill(COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Das Spiel ist vorbei ! Your score is {self.snake.lenght}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))

        pygame.display.flip()



    def play_sound(self, sound_name):
        if sound_name == "crash":
            audio = pygame.mixer.Sound("crash.mp3")
        elif sound_name == 'ding':
            audio = pygame.mixer.Sound("ding.mp3")

        pygame.mixer.Sound.play(audio)

    def play(self):
        self.snake.walk()
        self.food.draw()
        self.display_score()
        pygame.display.flip()



        # Schlange isst Essen
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.play_sound("ding")
            self.snake.increase_lenght()
            self.food.move()

        # Schlange isst er
        for i in range(2, self.snake.lenght):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')


            # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 950 and 0 <= self.snake.y[0] <= 600):
            exit(0)

    def running(self):

        run = True
        pause = False

        while run:
            for event in pygame.event.get():
                # if you want use a special letter do
                if event.type == KEYDOWN:
                    if event.type == K_ESCAPE:
                        run = False
                        # pass

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:
                    run = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True

            time.sleep(.4)

if __name__ == "__main__":

    game = Game()
    game.running()
    pygame.display.flip()


