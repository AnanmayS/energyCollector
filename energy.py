import pygame
import random
import sys 
pygame.init()
class Game:
    screen = None
    items = []
    collector = []
    lost = False

    def __init__(self, width, height, score, lives):
        self.score = score
        self.width = width
        self.lives = lives
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        done = False

        player = Player(self, width / 2 + 100, height - 20)
        generator = iGEN(self)
        collect = None
        score = 0
        pygame.display.update()
        while done == False:
            self.showStats()
            if len(self.items) == 0:
                self.displayText("VICTORY ACHIEVED")

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:  
                player.x -= 4 if player.x > 20 else 0  
            elif pressed[pygame.K_RIGHT]:  
                player.x += 4 if player.x < width - 20 else 0  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.collector.append(Collect(self, player.x, player.y, 1))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not self.lost:
                    self.collector.append(Collect(self, player.x, player.y, 2))

            
            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            for item in self.items:
                item.draw()
                item.checkCollision(self)
                if (item.y > height) or self.lives == 0:
                    self.lost = True
                    done = True
                    SplashScreenLost(self.score)

            for collect in self.collector:
                collect.draw()

            if not self.lost: player.draw()

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        resurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(resurface, (110, 160))
    
    def showStats(self):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 20)
        TotEng = font.render("Score: " + str(self.score), False, (255, 255,255))
        self.screen.blit(TotEng, (400, 10))
        TotLiv = font.render("Lives: " + str(self.lives), False, (255, 255,255))
        self.screen.blit(TotLiv, (100, 10))


class Item:

    def __init__(self, game, x, y, version):
        self.version = version
        self.x = x
        self.game = game
        self.y = y
        self.size = 30

    def draw(self):
        grey = (128, 128, 128)
        yellow = (225, 225, 0)
        if self.version == 1:
            pygame.draw.rect(self.game.screen, grey, pygame.Rect(self.x, self.y, self.size, self.size))
        elif self.version == 2:
            pygame.draw.rect(self.game.screen, yellow, pygame.Rect(self.x, self.y, self.size, self.size))
        self.y += 0.07

    def checkCollision(self, game):
        for collect in game.collector:
            if (collect.x < self.x + self.size and collect.x > self.x - self.size and collect.y < self.y + self.size and collect.y > self.y - self.size):
                if self.version == collect.version:
                    game.collector.remove(collect)
                    game.items.remove(self)
                    if self.version == 2:
                        game.score = game.score + 1
                        print(game.score)
                else:
                    game.collector.remove(collect)
                    game.lives -= 1


class Player:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y

    def draw(self):
        pygame.draw.rect(self.game.screen, (210, 250, 251), pygame.Rect(self.x, self.y, 8, 5))


class iGEN:
    def __init__(self, game):
        margin = 20
        width = 40
        for x in range(margin, game.width - margin, width):
            for y in range(margin+20, int(game.height / 2), width):
                game.items.append(Item(game, x, y, random.randint(1,2)))
    



class Collect:
    def __init__(self, game, x, y, version):
        self.version = version
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        red = (255, 0, 0)
        yel = (255, 255, 0)
        if self.version == 1:
            pygame.draw.rect(self.game.screen, red, pygame.Rect(self.x, self.y, 2, 8))
        elif self.version == 2:
            pygame.draw.rect(self.game.screen, yel, pygame.Rect(self.x, self.y, 2, 8))
        self.y -= 3

def SplashScreen():
    on = True
    while on:
        screen_width = 500
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 30)
        resurface = font.render("CO2 Defender", False, (255, 255, 255))
        font = pygame.font.SysFont('Arial', 19)
        start = font.render("Click Space to Destroy the CO2", False, (255, 255, 255))
        instruct = font.render("Click Enter to Grab the Solar Energy", False, (255, 255, 255))
        screen.blit(resurface, (150, 160))
        screen.blit(start, (120, 300))
        screen.blit(instruct, (99, 330))
        pygame.display.set_caption("Energy Harvester")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                newGame = Game(500, 600, 0 , 5)
                on = False

def SplashScreenLost(score):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    screen_width = 500
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    start = font.render("You Lost", False, (255, 255, 255))
    eng = font.render("Total Clean Energy: " + str(score) + " Watts", False, (255, 255, 255))
    screen.blit(start, (190, 300))
    screen.blit(eng, (70, 500))
    pygame.display.update()
    pygame.time.wait(5000)

if __name__ == '__main__':
    SplashScreen()