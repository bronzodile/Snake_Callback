import pygame
from pygame.math import Vector2
from utils import load_sprite, get_random_position
PADDING = 2

class Apple:
    def __init__(self,position,cell_size):
        self.position = Vector2(position)
        self.sprite = load_sprite("apple", True)
        self.sprite = pygame.transform.scale(self.sprite,(cell_size - PADDING * 2,cell_size - PADDING * 2))
        self.cell_size = cell_size
    
    def draw(self,surface):
        blit_position = self.position * self.cell_size + Vector2(PADDING)
        surface.blit(self.sprite,blit_position)

class Segment:
    def __init__(self,position,from_dir,to_dir):
        self.position = position
        self.from_dir = from_dir
        self.to_dir = to_dir 

class Python:
    def __init__(self,head_pointer,cell_size,direction,spawn_new_apple,field_dimensions):
        self.head_sprite = load_sprite("head", True)
        self.head_sprite = pygame.transform.scale(self.head_sprite,(cell_size - PADDING * 2,cell_size - PADDING * 2))        
        self.tail_sprite = load_sprite("tail",True)
        self.tail_sprite = pygame.transform.scale(self.tail_sprite,(cell_size - PADDING * 2,cell_size - PADDING * 2))                
        self.body_sprite = load_sprite("body", True)
        self.body_sprite = pygame.transform.scale(self.body_sprite,(cell_size - PADDING * 2,cell_size - PADDING * 2))                
        self.swing_sprite = load_sprite("swing", True)
        self.swing_sprite = pygame.transform.scale(self.swing_sprite,(cell_size - PADDING * 2,cell_size - PADDING * 2))                

        self.cell_size = cell_size
        self.prev_direction = direction
        self.direction = direction
        self.add_new_apple = spawn_new_apple
        self.field_dimensions = field_dimensions

        self.segments = []
        self.segments.append(Segment(Vector2(head_pointer),self.prev_direction,self.direction))
        curr_segment = self.segments[0]
        for _ in range(2):
            match direction:
                case "UP":
                    self.segments.append(Segment(self.next_position("DOWN",curr_segment.position),self.prev_direction,self.direction))
                case "DOWN":
                    self.segments.append(Segment(self.next_position("UP",curr_segment.position),self.prev_direction,self.direction))
                case "LEFT":
                    self.segments.append(Segment(self.next_position("RIGHT",curr_segment.position),self.prev_direction,self.direction))
                case "RIGHT":
                    self.segments.append(Segment(self.next_position("LEFT",curr_segment.position),self.prev_direction,self.direction))
            curr_segment = self.segments[-1]

    def draw(self,surface):
        
        blit_position = self.segments[0].position * self.cell_size + Vector2(PADDING)            
        surface.blit(self.head_sprite,blit_position)
        for segment in self.segments[1:-1]:
            blit_position = segment.position * self.cell_size + Vector2(PADDING)            
            surface.blit(self.body_sprite,blit_position)
        blit_position = self.segments[-1].position * self.cell_size + Vector2(PADDING)            
        surface.blit(self.tail_sprite,blit_position)

    def move(self, apple):
        new_head_position = self.next_position(self.direction,self.segments[0].position)
        if new_head_position == apple.position:
            temp_segments = list(self.segments)
            temp_segments.append(Segment(new_head_position,self.prev_direction,self.direction))
            spawn_collision = True
            while spawn_collision:
                new_apple_position = get_random_position(self.field_dimensions)
                spawn_collision = False
                for segment in temp_segments:
                    if segment.position == new_apple_position:
                        spawn_collision = True
            new_apple = Apple(new_apple_position,apple.cell_size)
            self.add_new_apple(new_apple)            
        else:
            self.segments.pop()
        self.segments.insert(0,Segment(new_head_position,self.prev_direction,self.direction))
        
    def turn(self,new_direction):
        for segment in self.segments:
            match new_direction:
                case "UP":
                    if self.direction != "UP" and self.direction != "DOWN":
                        self.direction = "UP"
                case "DOWN":
                    if self.direction != "UP" and self.direction != "DOWN":
                        self.direction = "DOWN"
                case "LEFT":
                    if self.direction != "LEFT" and self.direction != "RIGHT":
                        self.direction = "LEFT"
                case "RIGHT":
                    if self.direction != "LEFT" and self.direction != "RIGHT":
                        self.direction = "RIGHT"
                                                
    def next_position(self,direction,curr_position):
        match direction:
            case "UP":
                next_position = (curr_position[0],curr_position[1] - 1)
            case "DOWN":
                next_position = (curr_position[0],curr_position[1] + 1)
            case "LEFT":
                next_position = (curr_position[0] - 1,curr_position[1])
            case "RIGHT":
                next_position = (curr_position[0] + 1,curr_position[1])
        
        x, y = next_position
        w, h = self.field_dimensions
        return(Vector2(x % w, y % h))



