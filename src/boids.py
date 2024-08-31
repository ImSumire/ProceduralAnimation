from math import sqrt, pow, atan2, cos, sin, pi
from random import uniform

import pygame as pg


W, H = 1280, 720

pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
pg.display.set_caption("Boids")


AVOIDANCE = True  # avoid collisions
ALIGNMENT = True  # align nearby angles
COHESION = True  # find center of group


def dist2d(x1: float, y1: float, x2: float, y2: float) -> float:
    return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


class Boid:
    def __init__(self, x: float = 0.0, y: float = 0.0, angle: float = 0.0) -> None:
        self.x = x
        self.y = y

        self.angle = angle

        self.speed = uniform(0.9, 1.1)

        self.avoidAngle = 0.04
        self.alignAngle = 0.03
        self.cohesionAngle = 0.007

    def update(self):
        if AVOIDANCE:
            moveX = 0.0
            moveY = 0.0

            for other in boids:
                if (
                    other is not self
                    and dist2d(self.x, self.y, other.x, other.y) < 20.0
                ):
                    # Separation vector
                    moveX += self.x - other.x
                    moveY += self.y - other.y
            
            if moveX != 0.0 and moveY != 0.0:
                avoidAngle = atan2(moveY, moveX)

                # Adjust the current angle towards the avoid angle
                angleDiff = avoidAngle - self.angle
                # Normalize angle to range [-pi, pi]
                angleDiff = (angleDiff + pi) % (2 * pi) - pi

                if abs(angleDiff) > self.avoidAngle:
                    angleDiff = self.avoidAngle if angleDiff > 0.0 else -self.avoidAngle

                self.angle += angleDiff
        
        if ALIGNMENT:
            alignX = 0.0
            alignY = 0.0
            nearbyBoids = 0

            for other in boids:
                if (
                    other is not self
                    and dist2d(self.x, self.y, other.x, other.y) < 40.0 
                ):
                    # Alignment vector
                    alignX += cos(other.angle)
                    alignY += sin(other.angle)
                    nearbyBoids += 1
            
            if nearbyBoids > 0:
                averageAngle = atan2(alignY, alignX)
                alignDiff = (averageAngle - self.angle + pi) % (2 * pi) - pi

                if abs(alignDiff) > self.alignAngle:
                    alignDiff = self.alignAngle if alignDiff > 0 else -self.alignAngle

                self.angle += alignDiff
        
        if COHESION:
            cohesionX = 0.0
            cohesionY = 0.0
            nearbyBoids = 0

            for other in boids:
                if (
                    other is not self
                    and dist2d(self.x, self.y, other.x, other.y) < 80.0
                ):
                    # Cohesion vector (average position)
                    cohesionX += other.x
                    cohesionY += other.y
                    nearbyBoids += 1
            
            if nearbyBoids > 0:
                avgCohesionX = cohesionX / nearbyBoids
                avgCohesionY = cohesionY / nearbyBoids

                cohesionAngle = atan2(avgCohesionY - self.y, avgCohesionX - self.x)
                cohesionDiff = (cohesionAngle - self.angle + pi) % (2 * pi) - pi

                if abs(cohesionDiff) > self.cohesionAngle:
                    cohesionDiff = self.cohesionAngle if cohesionDiff > 0 else -self.cohesionAngle

                self.angle += cohesionDiff

        # Movement update
        self.x = (self.x + cos(self.angle) * self.speed) % W
        self.y = (self.y + sin(self.angle) * self.speed) % H

    def draw(self, surf: pg.Surface):
        pg.draw.circle(surf, (255, 255, 255), (self.x, self.y), 3.0)

        x = cos(self.angle)
        y = sin(self.angle)
        pg.draw.line(surf, (0, 128, 255), (self.x, self.y), (self.x + x * 8, self.y + y * 8), 3)


boids: list[Boid] = [
    Boid(uniform(0, W), uniform(0, H), uniform(-pi, pi))
    for _ in range(80)
]


while True:
    # Update
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    
    for boid in boids:
        boid.update()

    # Render
    screen.fill(0)

    for boid in boids:
        boid.draw(screen)

    pg.display.flip()
