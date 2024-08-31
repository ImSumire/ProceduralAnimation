from math import sqrt, pow
from random import randint

import pygame as pg


W, H = 1280, 720

pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
pg.display.set_caption("Procedural Animation")


def dist2d(x1: float, y1: float, x2: float, y2: float) -> float:
    return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


class Node:
    def __init__(self, x: float, y: float, gap: float, size: float) -> None:
        self.x = x
        self.y = y
        self.gap = gap
        self.size = size

        self.previous = None
    
    def update(self):
        if self.previous is not None:
            px, py = self.previous.x, self.previous.y
            distance = dist2d(self.x, self.y, px, py)

            if distance != 0.0:
                dirx = (self.x - px) / distance
                diry = (self.y - py) / distance

                self.x = px + dirx * self.gap
                self.y = py + diry * self.gap



class Entity:
    def __init__(self, x: float = 0.0, y: float = 0.0, length: int = 12, sizes: list[float] = [4.0], gaps: list[float] = [10.0], speed: float = 4.0) -> None:
        self.nodes: list[Node] = []
        self.head = Node(x, y, gaps[0], sizes[0])

        # Init nodes
        prevNode = self.head
        for i in range(length - 1):
            node = Node(0.0, 0.0, gaps[(i + 1) % len(gaps)], sizes[(i + 1) % len(sizes)])
            node.previous = prevNode
            self.nodes.append(node)
            prevNode = node
        
        self.length = length
        self.speed = speed
    
    def update(self):
        mx, my = pg.mouse.get_pos()
        # self.head.x = mx
        # self.head.y = my
        distance = dist2d(self.head.x, self.head.y, mx, my)

        if distance != 0.0:
            dirx = (self.head.x - mx) / distance
            diry = (self.head.y - my) / distance

            self.head.x -= dirx * self.speed
            self.head.y -= diry * self.speed

        for node in self.nodes:
            node.update()
    
    def draw(self, surf: pg.Surface):
        pg.draw.circle(surf, (255, 0, 0), (self.head.x, self.head.y), self.head.size, 1)

        for node in self.nodes:
            pg.draw.circle(surf, (255, 255, 255), (node.x, node.y), node.size, 1)


entities: list[Entity] = []
for _ in range(3):
    x = randint(0, W)
    y = randint(0, H)
    entities.append(Entity(x, y, sizes=[30.0, 35.0, 39.0, 39.0, 35.0, 30.0, 22.5, 16.0, 12.0, 10.0, 8.0, 6.0], gaps=[30.0]))

while True:
    # Update
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    for entity in entities:
        entity.update()

    # Render
    screen.fill(0)
    for entity in entities:
        entity.draw(screen)

    pg.display.flip()
