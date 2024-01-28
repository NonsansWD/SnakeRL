import pygame
import sys

class World:

    def __init__(self):
        self.width = 640
        self.height = 640
        self.blockSize = 40
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))
        

    def drawGrid(self):
        for x in range(0, self.width, self.blockSize):
            for y in range(0, self.height, self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
    
    def main(self):
        pygame.init()
        self.drawGrid()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

if __name__ == "__main__":
    w = World()
    w.main()