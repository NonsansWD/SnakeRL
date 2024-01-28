import pygame
import sys
import enum
import random


class Color(enum.Enum):
    WHITE = (255, 255, 255)
    GREY = (200, 200, 200)
    DARKGREY = (100, 100, 100)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class World:
    def __init__(self, width=640, height=640, blockSize=40):
        self.width = width
        self.height = height
        self.blockSize = blockSize
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))

        self.direction = Direction.RIGHT
        self.body = [  # slip into self.head and self.tail?
            Point(width / 2, height / 2),
            Point(width / 2 - self.blockSize, height / 2),
            Point(width / 2 - self.blockSize * 2, height / 2),
        ]
        self.food = self.setFood()

    def drawGrid(self):
        for x in range(0, self.width, self.blockSize):
            for y in range(0, self.height, self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, Color.DARKGREY.value, rect, 1)

    def drawSnake(self):
        pygame.draw.rect(
            self.screen,
            Color.WHITE.value,
            pygame.Rect(self.body[0].x, self.body[0].y, self.blockSize, self.blockSize),
        )

        for point in self.body[1:]:
            pygame.draw.rect(
                self.screen,
                Color.GREY.value,
                pygame.Rect(point.x, point.y, self.blockSize, self.blockSize),
            )

    def setFood(self):
        x = (
            random.randint(0, self.width - self.blockSize)
            // self.blockSize
            * self.blockSize
        )
        y = (
            random.randint(0, self.height - self.blockSize)
            // self.blockSize
            * self.blockSize
        )

        if Point(x, y) in self.body:  # if food is on the snake, try again
            self.setFood()
        self.food = Point(x, y)

    def drawFood(self):
        if self.food is None:  # can't draw food if there is none
            return

        pygame.draw.rect(
            self.screen,
            Color.RED.value,
            pygame.Rect(self.food.x, self.food.y, self.blockSize, self.blockSize),
        )

    def main(self):
        pygame.init()
        self.drawGrid()
        self.setFood()  # why is this needed, self.food is already set in __init__?
        self.drawFood()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_UP:
                            self.direction = Direction.UP
                        case pygame.K_DOWN:
                            self.direction = Direction.DOWN
                        case pygame.K_LEFT:
                            self.direction = Direction.LEFT
                        case pygame.K_RIGHT:
                            self.direction = Direction.RIGHT
            self.drawSnake()

            pygame.display.update()


if __name__ == "__main__":
    w = World()
    w.main()
