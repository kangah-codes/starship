import pygame

screen = pygame.display.set_mode((600, 500))
pygame.init()

class FadingText():
    def __init__(self, text, color, size, fadespeed):
        self.text = text
        self.color = color
        self.size = size
        self.speed = fadespeed
        self.font = pygame.font.SysFont("Monaco", self.size)
        self.rendered = None
        self.alpha = 255

    def render(self):
        self.rendered = self.font.render(f"{self.text}", True, self.color)

        #screen.blit(self.rendered, (100,100))

    def fade(self):
        x, y = 100, 100
        temp = pygame.Surface((self.rendered.get_width(), self.rendered.get_height())).convert()
        temp.blit(screen, (-x,-y))
        temp.blit(self.rendered, (0,0))
        if self.alpha > 0:
            temp.set_alpha(self.alpha)
            self.alpha -= .5
            screen.blit(temp, (100,100))
        

f = FadingText("LOLS", [255,255,255], 32, 10)

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()

    screen.fill((0,0,0))

    f.render()
    f.fade()

    pygame.display.update()