import array
from typing import Callable
from random import randint
from enum import Enum

import pygame


COLOR_FIELD = (30, 119, 109)  # #1E776D
COLOR_FONT = (255, 255, 255)  # #FFFFFF
COLOR_EMPTY = (0, 158, 142)  # #009E8E

COLOR_BORDER = (255, 174, 115)  # #FFAE73
COLOR_FLAG = (255, 108, 0)  # #FF6C00

COLOR_BUTTON = (166, 70, 0)  # #A64600
COLOR_MENU = (191, 109, 48)  # #BF6D30


class CellState(Enum):
    EMPTY = 0
    BOMB = 1
    FLAG = 2
    FLAGED_BOMB = 3
    OPENED = 4


class GameStatus(Enum):
    RUNNING = 0
    LOST = 1
    WIN = 2


class PixelFont:
    def __init__(self, number) -> None:
        self.number = number

    def render(self, screen, rect: pygame.rect.Rect) -> None:
        match self.number:
            case 1:
                start = (rect.left + rect.width // 2, rect.top + rect.height * 0.1) 
                end = (rect.left + rect.width // 2, rect.top + rect.height * 0.9)
                pygame.draw.line(screen, COLOR_FONT, start, end, 5)
            case 2:
                points = [
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.1),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.1),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.4),
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.9),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.9),
                ]
                pygame.draw.lines(screen, COLOR_FONT, False, points, 5)
            case 3:
                points = [
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.1),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.1),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.9),
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.9),
                ]
                pygame.draw.lines(screen, COLOR_FONT, False, points, 5)
                pygame.draw.line(
                    screen,
                    COLOR_FONT,
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.45),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.45),
                    5,
                )
            case 4:
                points = [
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.1),
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.45),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.45),
                ]
                pygame.draw.lines(screen, COLOR_FONT, False, points, 5)
                pygame.draw.line(
                    screen,
                    COLOR_FONT,
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.1),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.9),
                    5,
                )
            case 5:
                points = [
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.1),
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.1),
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.45),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.45),
                    (rect.left + rect.width * 0.9, rect.top + rect.height * 0.9),
                    (rect.left + rect.width * 0.1, rect.top + rect.height * 0.9),
                ]
                pygame.draw.lines(screen, COLOR_FONT, False, points, 5)
            case 6:
                ...
            case 7:
                ...
            case 8:
                ...
            case 9:
                ...
            case 0:
                ...


class MessageBox:
    def __init__(
            self,
            left,
            top,
            width,
            height,
            message,
            button_text,
            callback: Callable,
        ) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        
        self.menu_rect = pygame.rect.Rect(self.left, self.top, self.width, self.height)
        self.button_rect = pygame.rect.Rect(
            self.left + self.width * 0.25,
            self.top + self.height * 0.7,
            self.width * 0.5,
            self.height * 0.2,
        )

        self.message = message
        self.button_text = button_text
        self.message_render = pygame.font.SysFont("Open Sans", 36) \
            .render(self.message, True, COLOR_FONT)
        self.button_text_render = pygame.font.SysFont("Open Sans", 36) \
            .render(self.button_text, True, COLOR_FONT)
        
        self.message_rect = self.message_render.get_rect(center=(
            self.menu_rect.left + self.menu_rect.width / 2,
            self.menu_rect.top + self.menu_rect.height / 2,
        ))
        self.button_text_rect = self.button_text_render.get_rect(center=(
            self.button_rect.left + self.button_rect.width / 2,
            self.button_rect.top + self.button_rect.height / 2,
        ))

        self.callback = callback

    def check_collision(self, x, y) -> None:
        if (
            (self.button_rect.left < x < self.button_rect.right) and
            (self.button_rect.top < y < self.button_rect.bottom)
        ):
            return True
        return False

    def update(self, x, y) -> None:
        if self.check_collision(x, y):
            self.callback()

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, COLOR_MENU, self.menu_rect, border_radius=5)
        pygame.draw.rect(screen, COLOR_BUTTON, self.button_rect, border_radius=5)
        screen.blit(self.message_render, self.message_rect)
        screen.blit(self.button_text_render, self.button_text_rect)


class Field:
    def __init__(
            self,
            rows: int,
            cols: int,
            screen_height: int,
            screen_width: int,
            num_mines: int,
        ) -> None:
        self.rows = rows
        self.cols = cols
        self.cell_height = screen_height / self.rows
        self.cell_width = screen_width / self.cols
        self.num_mines = num_mines
        self.flags = 0
        self.flaged_bombs = 0
        self.empty_cells = self.rows * self.cols

        self.field = [
            array.array("i", [CellState.EMPTY.value] * cols) for _ in range(rows)
        ]
        self.mines_count_filed = [array.array("i", [0] * cols) for _ in range(rows)]

        i = 0
        while i < self.num_mines:
            x, y = randint(0, cols - 1), randint(0, rows - 1)
            if self.field[x][y] == CellState.BOMB.value:
                continue
            self.field[x][y] = CellState.BOMB.value
            i += 1

        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col] == CellState.BOMB.value:
                    continue
                bomb_count = 0
                for dy in range(row - 1, row + 2):
                    for dx in range(col - 1, col + 2):
                        if dy < 0 or dy >= self.rows or dx < 0 or dx >= self.cols:
                            continue
                        if self.field[dy][dx] == CellState.BOMB.value:
                            bomb_count += 1
                self.mines_count_filed[row][col] = bomb_count

    def update(self) -> None:
        ...

    def render(self, screen: pygame.Surface) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col] == CellState.OPENED.value:
                    cell = pygame.Rect(
                        col * self.cell_width + 2,
                        row * self.cell_height + 2,
                        self.cell_width - 2,
                        self.cell_height - 2,
                    )
                    pygame.draw.rect(
                        screen,
                        COLOR_EMPTY,
                        cell,
                    )
                    if self.mines_count_filed[row][col] != 0:
                        PixelFont(self.mines_count_filed[row][col]).render(screen, cell)
                elif self.field[row][col] in (CellState.FLAG.value, CellState.FLAGED_BOMB.value):
                    cell = pygame.Rect(
                        col * self.cell_width + 2,
                        row * self.cell_height + 2,
                        self.cell_width - 2,
                        self.cell_height - 2,
                    )
                    pygame.draw.rect(
                        screen,
                        COLOR_FLAG,
                        cell,
                    )

        for row in range(self.rows):
            pygame.draw.line(
                screen,
                COLOR_BORDER,
                (0, row * self.cell_height),
                (screen.get_width(), row * self.cell_height),
                2,
            )

        for col in range(self.cols):
            pygame.draw.line(
                screen,
                COLOR_BORDER,
                (col * self.cell_width, 0),
                (col * self.cell_width, screen.get_height()),
                2,
            )

    def open_cell(self, x, y, visited=None) -> None:
        if visited is None:
            visited = set()
        if (x, y) in visited:
            return

        if self.field[y][x] != CellState.EMPTY.value:
            return

        self.field[y][x] = CellState.OPENED.value
        self.empty_cells -= 1
        visited.add((x, y))
        if self.mines_count_filed[y][x] != 0:
            return
        for dy in range(y - 1, y + 2):
            for dx in range(x - 1, x + 2):
                if dy < 0 or dy >= self.rows or dx < 0 or dx >= self.cols:
                    continue
                self.open_cell(dx, dy, visited)

    def is_bomb(self, x, y) -> bool:
        return self.field[y][x] == CellState.BOMB.value

    def set_flag(self, x, y) -> None:
        if self.field[y][x] == CellState.BOMB.value:
            self.field[y][x] = CellState.FLAGED_BOMB.value
            self.flaged_bombs += 1
            self.empty_cells -= 1
        elif self.field[y][x] == CellState.FLAGED_BOMB.value:
            self.field[y][x] = CellState.BOMB.value
            self.flaged_bombs -= 1
            self.empty_cells += 1
        elif self.field[y][x] == CellState.EMPTY.value:
            self.field[y][x] = CellState.FLAG.value
            self.flags += 1
            self.empty_cells -= 1
        elif self.field[y][x] == CellState.FLAG.value:
            self.field[y][x] = CellState.EMPTY.value
            self.flags -= 1
            self.empty_cells += 1

    def is_won(self) -> bool:
        if self.empty_cells == 0 and (self.flaged_bombs + self.flags) == self.num_mines:
            return True
        return False


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption("Minesweeper")
        self.width = 1200
        self.height = 1200
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.running = True
        self.status = GameStatus.RUNNING
        self.field = Field(9, 9, self.height, self.width, 10)
        self.menu = {
            GameStatus.WIN: MessageBox(
                self.width * 0.25,
                self.height * 0.25,
                self.width * 0.5,
                self.height * 0.5,
                "You win!",
                "Ok!",
                self._restart,
            ),
            GameStatus.LOST: MessageBox(
                self.width * 0.25,
                self.height * 0.25,
                self.width * 0.5,
                self.height * 0.5,
                "You loose!",
                "Ok!",
                self._restart,
            )
        }
    
    def _restart(self) -> None:
        self.field = Field(9, 9, self.height, self.width, 10)
        self.status = GameStatus.RUNNING

    def _handle_event(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.status == GameStatus.RUNNING:
                        x = int(x // self.field.cell_width)
                        y = int(y // self.field.cell_height)
                        match event.button:
                            case pygame.BUTTON_LEFT:
                                if self.field.is_bomb(x, y):
                                    self.status = GameStatus.LOST
                                else:
                                    self.field.open_cell(x, y)
                            case pygame.BUTTON_RIGHT:
                                self.field.set_flag(x, y)
                    else:
                        self.menu[self.status].update(x, y)
                        

    def _update(self) -> None:
        self.status = GameStatus.WIN if self.field.is_won() else self.status

    def _render(self) -> None:
        self.screen.fill(COLOR_FIELD)
        self.field.render(self.screen)
        if self.status == GameStatus.WIN:
            self.menu[self.status].render(self.screen)
        elif self.status == GameStatus.LOST:
            self.menu[self.status].render(self.screen)
        pygame.display.flip()
        self.delta_time = self.clock.tick(60) / 1000

    def run(self) -> None:
        while self.running:
            self._handle_event()
            self._update()
            self._render()
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
