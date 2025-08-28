import pygame
import sys
import random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(-1, 0)
        self.new_block = False

        # Load head images
        self.head_up = pygame.image.load(
            'graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'graphics/head_left.png').convert_alpha()

        # Load tail images
        self.tail_up = pygame.image.load(
            'graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'graphics/tail_left.png').convert_alpha()

        # Load body images
        self.body_vertical = pygame.image.load(
            'graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load(
            'graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                prev_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if prev_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (prev_block.x == -1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (prev_block.x == 1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif (prev_block.x == -1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (prev_block.x == 1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.image = pygame.image.load('graphics/apple.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.randomize()

    def draw_fruit(self):
        screen.blit(self.image, (int(self.pos.x * cell_size),
                    int(self.pos.y * cell_size)))

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.snake.update_head_graphics()
        self.snake.update_tail_graphics()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        head = self.snake.body[0]
        if not 0 <= head.x < cell_number or not 0 <= head.y < cell_number:
            self.game_over()
        if head in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


# Game setup
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction != Vector2(0, 1):
                main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and main_game.snake.direction != Vector2(0, -1):
                main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT and main_game.snake.direction != Vector2(1, 0):
                main_game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and main_game.snake.direction != Vector2(-1, 0):
                main_game.snake.direction = Vector2(1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
