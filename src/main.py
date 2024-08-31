from math import sqrt, pow, atan2, sin, cos, pi
from random import randint
from enum import Enum

import pygame as pg


W, H = 1280, 720

pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
pg.display.set_caption("Procedural Animation")


def dist2d(x1: float, y1: float, x2: float, y2: float) -> float:
    return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


class Movement(Enum):
    FOLLOW = 0
    AT = 1


class Render(Enum):
    CIRCLE = 0
    DEBUG = 1
    SHAPED = 2


RENDER = Render.DEBUG


class HeadNode:
    def __init__(self, entity: "Entity", x: float, y: float, size: float) -> None:
        self.entity = entity

        self.x = x
        self.y = y
        self.size = size

        self.next: Node = None

        # Angle constraint
        self.angle = 0.0
        self.angleLimit = 0.1
    
    def update(self):
        # Artificial Intelligence/Dumbness
        mx, my = pg.mouse.get_pos()

        if self.entity.movement == Movement.AT:
            self.x = mx
            self.y = my
        
        elif self.entity.movement == Movement.FOLLOW:
            distance = dist2d(self.x, self.y, mx, my)

            if distance > 38:  # idk why
                targetAngle = atan2(my - self.y, mx - self.x)
                angleDiff = (targetAngle - self.angle + pi) % (2 * pi) - pi

                # Apply angle constraint
                if abs(angleDiff) > self.angleLimit:
                    angleDiff = self.angleLimit if angleDiff > 0.0 else -self.angleLimit
                
                self.angle += angleDiff


                dirx = cos(self.angle)
                diry = sin(self.angle)

                self.x += dirx * self.entity.speed
                self.y += diry * self.entity.speed
    
    def draw(self, surf: pg.Surface):
        if RENDER == Render.CIRCLE:
            # Draw node
            pg.draw.circle(surf, (255, 255, 255), (self.x, self.y), self.size, 1)
        
        elif RENDER == Render.DEBUG:
            # Goal position
            gx, gy = pg.mouse.get_pos()

            # Node angle
            angle = atan2(gy - self.y, gx - self.x)
            x = cos(angle)
            y = sin(angle)
                
            # Draw angle vector
            pg.draw.circle(surf, (255, 255, 255), (self.x, self.y), 1.0)
            pg.draw.line(surf, (0, 128, 255), (self.x, self.y), (self.x + x * 8, self.y + y * 8))

            # Draw shape points
            pg.draw.circle(surf, (0, 255, 128), (self.x + x * self.size, self.y + y * self.size), 2.0)

            angleLeft = angle + 1.570796327  # pi / 2
            xLeft = cos(angleLeft)
            yLeft = sin(angleLeft)
            pg.draw.circle(surf, (0, 255, 128), (self.x + xLeft * self.size, self.y + yLeft * self.size), 2.0)
                
            angleRight = angle - 1.570796327  # pi / 2
            xRight = cos(angleRight)
            yRight = sin(angleRight)
            pg.draw.circle(surf, (0, 255, 128), (self.x + xRight * self.size, self.y + yRight * self.size), 2.0)



class Node:
    def __init__(self, x: float, y: float, gap: float, size: float) -> None:
        self.x = x
        self.y = y
        self.gap = gap
        self.size = size

        self.previous: HeadNode | Node = None
    
    def update(self):
        if self.previous is not None:
            # Distance constraint
            px, py = self.previous.x, self.previous.y
            distance = dist2d(self.x, self.y, px, py)

            if distance != 0.0:
                dirx = (self.x - px) / distance
                diry = (self.y - py) / distance

                self.x = px + dirx * self.gap
                self.y = py + diry * self.gap

    def draw(self, surf):
        if RENDER == Render.CIRCLE:
            # Draw node
            pg.draw.circle(surf, (255, 255, 255), (self.x, self.y), self.size, 1)
        
        elif RENDER == Render.DEBUG:
            prev = self.previous

            # Node angle
            angle = atan2(prev.y - self.y, prev.x - self.x)
            x = cos(angle)
            y = sin(angle)

            # Draw link
            pg.draw.line(surf, (0, 0, 255), (self.x, self.y), (prev.x, prev.y))
                
            # Draw angle vector
            pg.draw.circle(surf, (255, 255, 255), (self.x, self.y), 1.0)
            pg.draw.line(surf, (0, 128, 255), (self.x, self.y), (self.x + x * 8, self.y + y * 8))

            # Draw shape points
            angleLeft = angle + 1.570796327  # pi / 2
            xLeft = cos(angleLeft)
            yLeft = sin(angleLeft)
            pg.draw.circle(surf, (0, 255, 128), (self.x + xLeft * self.size, self.y + yLeft * self.size), 2.0)
                
            angleRight = angle - 1.570796327  # pi / 2
            xRight = cos(angleRight)
            yRight = sin(angleRight)
            pg.draw.circle(surf, (0, 255, 128), (self.x + xRight * self.size, self.y + yRight * self.size), 2.0)


class Entity:
    def __init__(
            self,
            x: float = 0.0,
            y: float = 0.0,
            length: int = 12,
            sizes: list[float] = [4.0],
            gaps: list[float] = [10.0],
            speed: float = 4.0,
            movement: Movement = Movement.AT
        ) -> None:
        self.nodes: list[Node] = []
        self.head = HeadNode(self, x, y, sizes[0])

        # Init nodes
        prevNode = self.head
        for i in range(length - 1):
            node = Node(0.0, 0.0, gaps[(i + 1) % len(gaps)], sizes[(i + 1) % len(sizes)])
            node.previous = prevNode
            self.nodes.append(node)
            prevNode = node
        
        self.head.next = self.nodes[1]
        
        self.length = length
        self.speed = speed
        self.movement = movement
    
    def update(self):
        self.head.update()

        for node in self.nodes:
            node.update()
    
    def draw(self, surf: pg.Surface):
        self.head.draw(surf)

        for node in self.nodes:
            node.draw(surf)


entities: list[Entity] = []
for _ in range(1):
    x = randint(0, W)
    y = randint(0, H)
    entities.append(Entity(
        x,
        y,
        length=14,
        sizes=[26, 29, 20, 30, 34, 35, 32, 25, 14, 7, 5, 4, 3, 3],
        gaps=[25],
        movement=Movement.FOLLOW
    ))

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
