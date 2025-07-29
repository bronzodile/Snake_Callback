import pygame
from utils import load_sprite
from models import Python, Apple

class Snake:
    SQUARESIDE = 80
    WIDTH = 18
    HEIGHT = 10
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")

        self.screen = pygame.display.set_mode((self.WIDTH * self.SQUARESIDE,self.HEIGHT * self.SQUARESIDE))
        self.clock = pygame.time.Clock()
        self.background = load_sprite("field", False)
        self.background = pygame.transform.scale(self.background,(self.WIDTH * self.SQUARESIDE,self.HEIGHT * self.SQUARESIDE))
        self.python = Python((5,5),self.SQUARESIDE,"RIGHT",self.spawn_new_apple,(self.WIDTH,self.HEIGHT))
        self.apple = Apple((10,5),self.SQUARESIDE)

    def main_loop(self):
        while True:
            self._handle_input()
            self._game_logic()
            self._draw()

    def _handle_input(self):
        key_handled_this_turn = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if not key_handled_this_turn:
                    if event.key == pygame.K_UP:
                        self.python.turn("UP")
                        key_handled_this_turn = True
                    if event.key == pygame.K_DOWN:
                        self.python.turn("DOWN")
                        key_handled_this_turn = True                    
                    if event.key == pygame.K_LEFT:
                        self.python.turn("LEFT")
                        key_handled_this_turn = True
                    if event.key == pygame.K_RIGHT:
                        self.python.turn("RIGHT")   
                        key_handled_this_turn = True         

    def _game_logic(self):
        self.python.move(self.apple)

    def _draw(self):
        self.screen.blit(self.background,(0,0))
        for i in range(self.HEIGHT):
            pygame.draw.line(self.screen, (0,0,0), (0, i * self.SQUARESIDE), (self.WIDTH * self.SQUARESIDE, i * self.SQUARESIDE))
        for i in range(self.WIDTH):
            pygame.draw.line(self.screen, (0,0,0), (i * self.SQUARESIDE, 0), (i * self.SQUARESIDE,self.HEIGHT * self.SQUARESIDE))
        self.python.draw(self.screen)
        self.apple.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(1.25)

    def spawn_new_apple(self, new_apple):
        self.apple = new_apple
