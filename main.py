import pygame
import os
from random import choice
pygame.init()
pygame.display.set_caption('Тетрис')
size = width, height = (600, 900)
font = pygame.font.Font(None, 80)
screen = pygame.display.set_mode(size)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


FIGURES = ['Z', 'reverse_Z', 'L', 'reverse_L', 'I', 'cube', 'triple']
CUBES_IMAGES = [pygame.transform.scale(load_image('cube.png'), (35, 35)),
                pygame.transform.scale(load_image('cube1.png'), (35, 35)),
                pygame.transform.scale(load_image('cube2.png'), (35, 35)),
                pygame.transform.scale(load_image('cube3.png'), (35, 35))]
FON_IMAGE = pygame.transform.scale(load_image('fon.png'), (600, 900))


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[False] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x < self.left or y < self.top\
                or x > self.left + self.cell_size * self.width - 1\
                or y > self.top + self.cell_size * self.height - 1:
            return None
        else:
            return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]:
                    if i >= 0:
                        sprite = pygame.sprite.Sprite()
                        sprite.image = CUBES_IMAGES[self.board[i][j] - 1]
                        sprite.rect = sprite.image.get_rect()
                        sprite.rect.x = board.left + j * board.cell_size
                        sprite.rect.y = board.top + i * board.cell_size
                        cubes_sprites.add(sprite)


class Figure:
    def __init__(self, type):
        self.type = type
        self.centre_x = 5
        self.centre_y = 0
        self.pose = 0
        self.image_num = choice((1, 2, 3, 4))
        if self.type == 'Z':
            self.poses_elements = (((1, 1), (1, 0), (0, 0), (0, -1)),
                                   ((-1, 1), (0, 1), (0, 0), (1, 0)))
        elif self.type == 'reverse_Z':
            self.poses_elements = (((1, -1), (1, 0), (0, 0), (0, 1)),
                                   ((1, 1), (0, 1), (0, 0), (-1, 0)))
        elif self.type == 'L':
            self.poses_elements = (((1, -1), (0, -1), (0, 0), (0, 1)),
                                   ((-1, -1), (-1, 0), (0, 0), (1, 0)),
                                   ((-1, 1), (0, 1), (0, 0), (0, -1)),
                                   ((1, 1), (1, 0), (0, 0), (-1, 0)))
        elif self.type == 'reverse_L':
            self.poses_elements = (((1, 1), (0, 1), (0, 0), (0, -1)),
                                   ((1, -1), (1, 0), (0, 0), (-1, 0)),
                                   ((-1, -1), (0, -1), (0, 0), (0, 1)),
                                   ((-1, 1), (-1, 0), (0, 0), (1, 0)))
        elif self.type == 'I':
            self.poses_elements = (((0, -2), (0, -1), (0, 0), (0, 1)),
                                   ((-2, 0), (-1, 0), (0, 0), (1, 0)))
        elif self.type == 'cube':
            self.poses_elements = (((1, -1), (0, -1), (0, 0), (1, 0)),)
        elif self.type == 'triple':
            self.poses_elements = (((0, -1), (0, 1), (0, 0), (1, 0)),
                                   ((-1, 0), (1, 0), (0, 0), (0, -1)),
                                   ((0, -1), (0, 1), (0, 0), (-1, 0)),
                                   ((-1, 0), (1, 0), (0, 0), (0, 1)))
        self.get_elements()

    def can_go_right(self):
        for i in self.elements:
            if i[1] + 1 >= 10 or (board.board[i[0]][i[1] + 1] and i[0] >= 0):
                return False
        return True

    def can_go_left(self):
        for i in self.elements:
            if i[1] - 1 < 0 or (board.board[i[0]][i[1] - 1] and i[0] >= 0):
                return False
        return True

    def go_right(self):
        global cubes_sprites
        for i in self.elements:
            i[1] += 1
        self.centre_x += 1
        screen.fill((0, 0, 0))
        screen.blit(screen2, (0, 0))
        self.render()
        board.render()
        cubes_sprites.draw(screen)
        pygame.display.flip()

    def go_left(self):
        global cubes_sprites
        for i in self.elements:
            i[1] -= 1
        self.centre_x -= 1
        screen.fill((0, 0, 0))
        screen.blit(screen2, (0, 0))
        self.render()
        board.render()
        cubes_sprites.draw(screen)
        pygame.display.flip()

    def rotate_clockwise(self):
        self.pose += 1
        self.pose %= len(self.poses_elements)
        self.get_elements()
        for i in self.elements:
            if i[0] >= 20 or i[1] >= 10 or i[1] < 0 or (board.board[i[0]][i[1]] and i[0] >= 0):
                self.rotate_counterclockwise()
                break

    def rotate_counterclockwise(self):
        self.pose -= 1
        self.pose %= len(self.poses_elements)
        self.get_elements()
        for i in self.elements:
            if i[0] >= 20 or i[1] >= 10 or i[1] < 0 or (board.board[i[0]][i[1]] and i[0] >= 0):
                self.rotate_clockwise()
                break

    def fall(self):
        for i in self.elements:
            if i[0] + 1 >= 20 or (board.board[i[0] + 1][i[1]] and i[0] + 1 >= 0):
                return False
        for i in self.elements:
            i[0] += 1
        self.centre_y += 1
        return True

    def render(self):
        global cubes_sprites
        cubes_sprites = pygame.sprite.Group()
        for i in self.elements:
            if i[0] >= 0:
                sprite = pygame.sprite.Sprite()
                sprite.image = CUBES_IMAGES[self.image_num - 1]
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = board.left + i[1] * board.cell_size
                sprite.rect.y = board.top + i[0] * board.cell_size
                cubes_sprites.add(sprite)

    def render_next(self):
        global next_figure_sprites
        next_figure_sprites = pygame.sprite.Group()
        for i in self.elements:
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.transform.scale(CUBES_IMAGES[self.image_num - 1], (20, 20))
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = i[1] * 20 - 48
            sprite.rect.y = 180 + i[0] * 20
            next_figure_sprites.add(sprite)

    def get_elements(self):
        self.elements = []
        for i in self.poses_elements[self.pose]:
            self.elements.append([self.centre_y + i[0], self.centre_x + i[1]])


def game_over():
    global level, need_count, count, lines, score
    level = 1
    need_count = ((0.8 - (level - 1) * 0.007) ** (level - 1)) * 120
    count = 0
    lines = 0
    score = 0
    screen2.blit(FON_IMAGE, (0, 0))
    next_figure.render_next()
    next_figure_sprites.draw(screen2)
    text = font.render(str(score), True, (255, 200, 0))
    text_w = text.get_width()
    text_h = text.get_height()
    screen2.blit(text, (300 - text_w // 2, 35 - text_h // 2))
    text = font.render(str(level), True, (230, 255, 0))
    text_w = text.get_width()
    text_h = text.get_height()
    screen2.blit(text, (543 - text_w // 2, 200 - text_h // 2))
    for i in range(20):
        for j in range(10):
            board.board[i][j] = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return


if __name__ == '__main__':
    board = Board(10, 20)
    board.set_view(130, 151, 34)
    cubes_sprites = pygame.sprite.Group()
    next_figure_sprites = pygame.sprite.Group()
    next_figure = Figure(choice(FIGURES))
    next_figure.render_next()
    figure = Figure(choice(FIGURES))
    figure.render()
    cubes_sprites.draw(screen)
    clock = pygame.time.Clock()
    level = 1
    need_count = ((0.8 - (level - 1) * 0.007) ** (level - 1)) * 120
    count = 0
    score = 0
    lines = 0
    screen2 = pygame.surface.Surface(size)
    screen2.blit(FON_IMAGE, (0, 0))
    next_figure_sprites.draw(screen2)
    text = font.render(str(score), True, (255, 200, 0))
    text_w = text.get_width()
    text_h = text.get_height()
    screen2.blit(text, (300 - text_w // 2, 35 - text_h // 2))
    text = font.render(str(level), True, (230, 255, 0))
    text_w = text.get_width()
    text_h = text.get_height()
    screen2.blit(text, (543 - text_w // 2, 200 - text_h // 2))
    screen.blit(screen2, (0, 0))
    pygame.display.flip()
    down_pressed = False
    left_pressed = False
    right_pressed = False
    running = True
    while running:
        clock.tick(120)
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if figure.can_go_left():
                        figure.go_left()
                        left_delay = 0
                        right_pressed = False
                        left_pressed = True
                if event.key == pygame.K_RIGHT:
                    if figure.can_go_right():
                        figure.go_right()
                        right_delay = 0
                        left_pressed = False
                        right_pressed = True
                if event.key == pygame.K_a:
                    figure.rotate_counterclockwise()
                if event.key == pygame.K_z:
                    figure.rotate_counterclockwise()
                if event.key == pygame.K_s:
                    figure.rotate_clockwise()
                if event.key == pygame.K_x:
                    figure.rotate_clockwise()
                if event.key == pygame.K_DOWN:
                    figure.fall()
                    down_delay = 0
                    down_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    down_pressed = False
                if event.key == pygame.K_LEFT:
                    left_pressed = False
                if event.key == pygame.K_RIGHT:
                    right_pressed = False
        if down_pressed:
            if down_delay < 60:
                down_delay += 1
                down_count = 0
            elif down_count % 5 != 0:
                down_count += 1
            else:
                down_count += 1
                figure.fall()
        if left_pressed:
            if left_delay < 60:
                left_delay += 1
                left_count = 0
            elif left_count % 10 != 0:
                left_count += 1
            else:
                left_count += 1
                if figure.can_go_left():
                    figure.go_left()
        if right_pressed:
            if right_delay < 60:
                right_delay += 1
                right_count = 0
            elif right_count % 10 != 0:
                right_count += 1
            else:
                right_count += 1
                if figure.can_go_right():
                    figure.go_right()
        if count >= need_count:
            count = 0
            if not figure.fall():
                down_pressed = False
                if board.board[0][5]:
                    game_over()
                else:
                    score += 30
                    for i in figure.elements:
                        board.board[i[0]][i[1]] = figure.image_num
                    figure = next_figure
                    next_figure = Figure(choice(FIGURES))
                    now_lines = 0
                    for i in range(board.height):
                        is_full = True
                        for j in range(board.width):
                            if not board.board[i][j]:
                                is_full = False
                        if is_full:
                            lines += 1
                            now_lines += 1
                            for k in range(i, 0, -1):
                                for j in range(board.width):
                                    board.board[k][j] = board.board[k - 1][j]
                            board.board[0] = [False] * board.width
                            level += lines // 8
                            lines %= 8
                            need_count = ((0.8 - (level - 1) * 0.007) ** (level - 1)) * 120
                    score += [0, 100, 300, 700, 1500][now_lines]
                    screen.fill((0, 0, 0))
                    screen2.blit(FON_IMAGE, (0, 0))
                    next_figure.render_next()
                    next_figure_sprites.draw(screen2)
                    text = font.render(str(score), True, (255, 200, 0))
                    text_w = text.get_width()
                    text_h = text.get_height()
                    screen2.blit(text, (300 - text_w // 2, 35 - text_h // 2))
                    text = font.render(str(level), True, (230, 255, 0))
                    text_w = text.get_width()
                    text_h = text.get_height()
                    screen2.blit(text, (543 - text_w // 2, 200 - text_h // 2))
                    screen.blit(screen2, (0, 0))
                    figure.render()
                    board.render()
                    cubes_sprites.draw(screen)
                    pygame.display.flip()
                    for i in figure.elements:
                        if board.board[i[0]][i[1]]:
                            game_over()
        screen.fill((0, 0, 0))
        screen.blit(screen2, (0, 0))
        figure.render()
        board.render()
        cubes_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()