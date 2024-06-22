from random import randint

import pygame as pg


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет по умолчанию
DEFAULT_COLOR = (150, 150, 150)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка. Выход из игры - ESC.')

# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color=DEFAULT_COLOR) -> None:
        """Инициализатор класса GameObject."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """
        Метод, который предназначен для переопределения в дочерних классах.

        Этот метод должен определять, как объект будет отрисовываться на
        экране. По умолчанию — pass.
        """
        raise NotImplementedError('Метод draw() не определен в '
                                  f'{self.__class__.__name__}!')

    def draw_cell(self, cell_position, body_color, border_color) -> None:
        """Метод, который отрисовывает ячейку на игровом поле."""
        rect = pg.Rect(cell_position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, busy_cell=[], body_color=APPLE_COLOR) -> None:
        """Инициализатор класса Apple."""
        super().__init__()
        self.body_color = body_color
        self.randomize_position(busy_cell)

    def randomize_position(self, busy_cell) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in busy_cell:
                break

    def draw(self) -> None:
        """Метод, который отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """Класс, описывающий змейку и действия с ней."""

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        """Инициализатор класса Snake."""
        super().__init__()
        self.reset()
        self.next_direction = None
        self.body_color = body_color

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Метод, который отвечает за движение змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        self.positions.insert(0,
                              ((head_x + GRID_SIZE * dir_x) % SCREEN_WIDTH,
                               (head_y + GRID_SIZE * dir_y) % SCREEN_HEIGHT))

        if self.length < len(self.positions):
            self.last = self.positions.pop(-1)
        else:
            self.last = None

    def draw(self) -> None:
        """Метод, который отрисовывает змейку на игровом поле."""
        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last,
                           BOARD_BACKGROUND_COLOR,
                           BOARD_BACKGROUND_COLOR)

        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position(), self.body_color, BORDER_COLOR)

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]


def handle_keys(game_object) -> None:
    """Метод, который обрабатывает нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                return False
    return True


def main() -> None:
    """Основной цикл игры."""
    pg.init()
    snake = Snake()
    apple = Apple(busy_cell=snake.positions)

    while True:
        clock.tick(SPEED)
        snake.move()
        if snake.get_head_position() in snake.positions[3:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        elif apple.position in snake.positions:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if not handle_keys(snake):
            break
        snake.update_direction()
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
