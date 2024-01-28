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
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.body = [  # split into self.head and self.tail?
            Point(width / 2, height / 2),
            Point(width / 2 - self.blockSize, height / 2),
            Point(
                width / 2 - self.blockSize * 2, height / 2
            ),  # black square at end of tail
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
            pygame.Rect(
                self.body[0].x + 1,
                self.body[0].y + 1,
                self.blockSize - 2,
                self.blockSize - 2,
            ),
        )

        for point in self.body[1:-1]:
            pygame.draw.rect(
                self.screen,
                Color.GREY.value,
                pygame.Rect(
                    point.x + 1, point.y + 1, self.blockSize - 2, self.blockSize - 2
                ),
            )
        # clean up the tail
        pygame.draw.rect(
            self.screen,
            Color.BLACK.value,
            pygame.Rect(
                self.body[-1].x + 1,
                self.body[-1].y + 1,
                self.blockSize - 2,
                self.blockSize - 2,
            ),
        )

    def getRandPoint(self):
        x = (random.randint(0, self.width) // self.blockSize) * self.blockSize
        y = (random.randint(0, self.height) // self.blockSize) * self.blockSize
        return Point(x, y)

    def setFood(self):
        newPoint = self.getRandPoint()
        while newPoint in self.body:  # if food is on the snake, try again
            newPoint = self.getRandPoint()
        self.food = newPoint

    def drawFood(self):
        if self.food is None:  # can't draw food if there is none
            return

        pygame.draw.rect(
            self.screen,
            Color.RED.value,
            pygame.Rect(
                self.food.x + 1, self.food.y + 1, self.blockSize - 2, self.blockSize - 2
            ),
        )

    def move(self):
        head = self.body[0]
        x = head.x
        y = head.y
        if self.direction == Direction.UP:
            if y <= 0:
                y = self.height
            y -= self.blockSize
        elif self.direction == Direction.DOWN:
            if y >= self.height - self.blockSize:
                y = -self.blockSize
            y += self.blockSize
        elif self.direction == Direction.LEFT:
            if x <= 0:
                x = self.width
            x -= self.blockSize
        elif self.direction == Direction.RIGHT:
            if x >= self.width - self.blockSize:
                x = -self.blockSize
            x += self.blockSize
        self.body.insert(0, Point(x, y))
        self.body.pop()

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
                            if self.direction == Direction.DOWN:
                                break
                            self.direction = Direction.UP
                        case pygame.K_DOWN:
                            if self.direction == Direction.UP:
                                break
                            self.direction = Direction.DOWN
                        case pygame.K_LEFT:
                            if self.direction == Direction.RIGHT:
                                break
                            self.direction = Direction.LEFT
                        case pygame.K_RIGHT:
                            if self.direction == Direction.LEFT:
                                break
                            self.direction = Direction.RIGHT
            self.drawSnake()
            self.move()
            pygame.display.update()

            # time is an illusion
            self.clock.tick(10)


if __name__ == "__main__":
    w = World()
    w.main()
