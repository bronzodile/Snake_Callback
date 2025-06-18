from pathlib import Path
from pygame.image import load
from pygame.math import Vector2
import random

def load_sprite(name, with_alpha=True):
    filename = Path(__file__).parent / Path("assets/sprites/" + name + ".png")
    sprite = load(filename.resolve())

    if with_alpha:
        return sprite.convert_alpha()
    
    return sprite.convert()

def get_random_position(dimensions):
    return Vector2(random.randrange(dimensions[0]),random.randrange(dimensions[1]))