import pygame as pg
import random

HEIGHT, WIDTH = 800, 800
cell_size, grid_width, grid_height = 32, 32, 32
WHITE = 255, 255, 255
GREEN = 0, 255, 0
BLACK = 0, 0, 0

class Game:
    def __init__(self, dim: tuple[int, int]) -> None:
        pg.init()
        self.screen = pg.display.set_mode(dim)
        self.Clock = pg.time.Clock()
        self.running = True
        self.spots = set()

    def display_grid(self):
        self.screen.fill(BLACK)
        for spot in self.spots:
            x, y = spot
            left = (x * cell_size, y * cell_size)
            pg.draw.rect(self.screen, GREEN, (*left, cell_size, cell_size ))
         

        for x in range(0, WIDTH, cell_size):
            for y in range(0, HEIGHT, cell_size):
                rect = pg.Rect(x, y, cell_size, cell_size)
                pg.draw.rect(self.screen, WHITE, rect, 1)


    def update_grid(self):
        all_neighbors = set()
        new_pos = set()
        for spot in self.spots:
            neighbors = self.get_neighbors(spot)
            all_neighbors.update(neighbors)

            neighbors = list(filter(lambda x: x in self.spots, neighbors))

            if len(neighbors) in [2,3]:
                new_pos.add(spot)

        for spot in all_neighbors:
            neighbors = self.get_neighbors(spot)
            neighbors = list(filter(lambda x: x in self.spots, neighbors))

            if len(neighbors) == 3:
                new_pos.add(spot)
        
        return new_pos


    def get_neighbors(self, spot):
        x, y = spot
        neighbors = []

        for dx in [-1, 0, 1]:
            if x + dx < 0 or x + dx > WIDTH:
                continue
            for dy in [-1, 0, 1]:
                if y + dy < 0 or y + dy > HEIGHT:
                    continue
                
                if dx == 0 and dy == 0:
                    continue
                neighbors.append((x + dx, y + dx))

        return neighbors

    def generateSpots(self, n):
        return set([(random.randrange(0, WIDTH // cell_size), random.randrange(0, HEIGHT // cell_size)) for _ in range(n)])

    def run(self):
        count = 0
        while self.running:
            freq = 60
            if count >= freq:
                count = 0
                self.spots = self.update_grid()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            
                if event.type == pg.MOUSEBUTTONDOWN:
                    x,y = pg.mouse.get_pos()
                    col = x//cell_size
                    row = y//cell_size
                    pos = (col, row)
                    
                    if pos in self.spots:
                        self.spots.remove(pos)
                    else: 
                        self.spots.add(pos)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        self.spots = set()

                    if event.key == pg.K_SPACE:
                        self.spots = self.generateSpots(random.randrange(2,5) * cell_size)
            count += 1
            self.display_grid()
            pg.display.update()
            self.Clock.tick(60)
            



def main():
    game = Game((HEIGHT, WIDTH))
    game.run()
    pg.quit()
if "__main__" == __name__:
    main()