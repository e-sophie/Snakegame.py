import pygame
import sys
import random
from pygame.math import Vector2


# Game setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Fonts/BADABB__.TTF', 25)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.head_up = pygame.image.load(
            'graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'graphics/head_left.png').convert_alpha()
        self.tail_up = pygame.image.load(
            'graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'graphics/tail_left.png').convert_alpha()
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
        self.crunch_sound = pygame.mixer.Sound('Sounds/crunch.mp3')

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

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        try:
            self.image = pygame.image.load(
                'graphics/apple.png').convert_alpha()
            self.image = pygame.transform.scale(
                self.image, (cell_size, cell_size))
        except:
            self.image = None
        self.randomize()

    def draw_fruit(self):
        if self.image:
            screen.blit(self.image, (int(self.pos.x * cell_size),
                        int(self.pos.y * cell_size)))
        else:
            fruit_rect = pygame.Rect(
                int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

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
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        head = self.snake.body[0]
        if not 0 <= head.x < cell_number or not 0 <= head.y < cell_number:
            self.game_over()
        if head in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(
                        col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 72, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        # Position apple image to the left of the score
        apple_image = self.fruit.image
        apple_rect = apple_image.get_rect(
            midright=(score_rect.left - 10, score_rect.centery))

        # Background rectangle behind apple and score
        padding = 10
        left = apple_rect.left - padding
        top = min(apple_rect.top, score_rect.top) - padding
        width = apple_rect.width + score_rect.width + 3 * padding
        height = max(apple_rect.height, score_rect.height) + 2 * padding
        bg_rect = pygame.Rect(left, top, width, height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        pygame.draw.rect(screen, (56, 72, 12), bg_rect, 2)
        screen.blit(score_surface, score_rect)
        screen.blit(apple_image, apple_rect)

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
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

    def check_fail(self):
        head = self.snake.body[0]
        if not 0 <= head.x < cell_number or not 0 <= head.y < cell_number:
            self.game_over()
        if head in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)


main_game = MAIN()


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
