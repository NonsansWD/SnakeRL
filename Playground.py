import pygame
import sys
import enum
import random
import Rewards as reward_class
import DQN


def wrapper(direction):
    if direction.name == Direction.UP.name:
        test = 0
    elif direction.name == Direction.LEFT.name:
        test = 1
    elif direction.name == Direction.DOWN.name:
        test = 2
    elif direction.name == Direction.RIGHT.name:
        test = 3
    return test


class Color(enum.Enum):
    WHITE = (255, 255, 255)
    GREY = (200, 200, 200)
    DARKGREY = (100, 100, 100)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)


class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y


class World:
    def __init__(self, width=640, height=640, blockSize=40):
        self.width = width
        self.height = height
        self.blockSize = blockSize
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()

    def drawGrid(self):
        for x in range(0, self.width, self.blockSize):
            for y in range(0, self.height, self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, Color.DARKGREY.value, rect, 1)
        pygame.display.update()

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

    def ai_move(self, direction):
        head = self.body[0]
        x, y = head.x, head.y
        # self.direction = direction
        # print(direction == Direction.UP.value)

        match direction:
            case 0:
                if self.direction != Direction.DOWN:
                    self.direction = Direction.UP
            case 1:
                if self.direction != Direction.UP:
                    self.direction = Direction.DOWN
            case 2:
                if self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
            case 3:
                if self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
        self.current_state = x, y, self.food.x, self.food.y, self.direction.value, self.terminal

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
        # self.wrapped_direction = wrapper(direction)
        if self.terminal == 1:
            self.terminal = 0
        self.new_state = self.body[0].x, self.body[0].y, self.food.x, self.food.y, self.direction.value, self.terminal
        self.terminal = 0
        reward = reward_class.DefaultReward.reward(self.current_state, self.new_state)
        pygame.display.set_caption(f"Snake | Score: {self.score}")
        self.drawSnake()
        pygame.display.update()

        return self.new_state, reward, self.terminal
        

    def foodCollision(self):
        if self.food == self.body[0]:
            self.terminal = 1
            self.score += 1
            self.setFood()
            self.drawFood()
            self.body.append(self.body[-1])
            # self.wrapped_direction = wrapper(self.direction)
            self.current_state = self.body[0].x, self.body[0].y, self.food.x, self.food.y, self.direction.value, self.terminal

    def checkCollision(self):
        if self.body[0] in self.body[1:-1]:
            self.terminal = 2
            return True
        else:
            return False
        # return self.body[0] in self.body[1:-1]

    def endScreen(self):
        pygame.display.set_caption(f"Snake Game | Score: {self.score} | GAME OVER")
        self.terminal = 2
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.K_SPACE:
                        self.__init__()
                        self.main()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


    def reset(self):
        pygame.init()
        self.screen.fill((0, 0, 0))
        self.direction = Direction.RIGHT
        self.body = [  # split into self.head and self.tail?
            Point(self.width / 2, self.height / 2),
            Point(self.width / 2 - self.blockSize, self.height / 2),
            Point(
                self.width / 2 - self.blockSize * 2, self.height / 2
            ),  # black square at end of tail
        ]
        self.setFood()
        self.score = 0
        self.terminal = 0
        # self.wrapped_direction = wrapper(self.direction)
        self.current_state = self.body[0].x, self.body[0].y, self.food.x, self.food.y, self.direction.value, self.terminal
        self.drawGrid()
        self.drawSnake()
        self.drawFood()


    def main(self):
        # setup
        pygame.init()
        self.reset()
        self.drawGrid()
        self.setFood()  # why is this needed, self.food is already set in __init__? cause its gay
        self.drawFood()
        # self.wrapped_direction = wrapper(self.direction)
        self.current_state = self.body[0].x, self.body[0].y, self.food.x, self.food.y, self.direction.value, self.terminal

        while True:
            # handle input
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
            # draw everything
            pygame.display.set_caption(f"Snake | Score: {self.score}")
            self.drawSnake()
            self.move()
            pygame.display.update()

            # cool guys look at explosions
            if self.checkCollision():
                self.endScreen()
            self.foodCollision()

            # time is an illusion
            self.clock.tick(10)


def train_model():
    world = World()
    episode_progress = DQN.deep_q_learning(world)
    print(episode_progress)


if __name__ == "__main__":
    # w = World()
    # w.main()
    train_model()