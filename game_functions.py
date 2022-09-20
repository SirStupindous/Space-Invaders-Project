import sys
import pygame as pg
from vector import Vector

movement = {pg.K_LEFT: Vector(-1, 0),   # dictionary to map keys to Vector velocities
            pg.K_RIGHT: Vector(1, 0),
            pg.K_UP: Vector(0, -1),
            pg.K_DOWN: Vector(0, 1)
            }
  
def check_keydown_events(event, settings, ship):
    key = event.key
    if key == pg.K_SPACE: 
        ship.shooting = True
    elif key in movement.keys(): ship.vel += settings.ship_speed_factor * movement[key]

def check_keyup_events(event, ship):
    key = event.key
    if key == pg.K_SPACE: ship.shooting = False
    elif key == pg.K_ESCAPE: ship.vel = Vector()   # Note: Escape key stops the ship
    # elif key in movement.keys(): ship.vel = Vector()

def check_events(settings, ship):
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.KEYDOWN: 
            check_keydown_events(event=event, settings=settings, ship=ship)
        elif event.type == pg.KEYUP: check_keyup_events(event=event, ship=ship)

def clamp(posn, rect, settings):
    left, top = posn.x, posn.y
    width, height = rect.width, rect.height
    left = max(0, min(left, settings.screen_width - width))
    top = max(0, min(top, settings.screen_height - height))
    return Vector(x=left, y=top), pg.Rect(left, top, width, height)
