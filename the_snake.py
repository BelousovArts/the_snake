from random import randrange
import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
# GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
# GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None
    

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()
    

    def randomize_position(self) -> tuple[int, int]:
        random_width = randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
        random_height = randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
        return (random_width, random_height)


    def draw(self) -> None:
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    
    def update_direction(self) -> None:
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    

    def move(self) -> None:
        head_pos_x, head_pos_y = self.get_head_position()
        new_position = ((head_pos_x + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH, 
                        (head_pos_y + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT)
        
        if new_position in self.positions:
            self.reset()
            return
        
        self.positions.insert(0, new_position)
        self.last = self.positions[-1]
        
        if self.length < len(self.positions):
            self.positions.pop(-1)
            
        


    def draw(self) -> None:
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    
    def get_head_position(self) -> tuple[int, int]:
        return self.positions[0]


    def reset(self) -> None:
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        screen.fill(BOARD_BACKGROUND_COLOR)

def handle_keys(game_object) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        handle_keys(snake)
        clock.tick(SPEED)
        snake.move()
        if apple.position in snake.positions:
            snake.length += 1
            apple.position = apple.randomize_position()
        snake.update_direction()
        apple.draw()
        snake.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()
