import pygame
from api import API
from config import API_TOKEN

def get_coordinates(x: int, y: int, height: int):
    return x, height - y

def visualize(problem: dict):
    pygame.init()
    divide = 10
    
    width = problem['room_width'] / divide
    height = problem['room_height'] / divide
    stage_width = problem['stage_width'] / divide
    stage_height = problem['stage_height'] / divide
    stage_left = problem['stage_bottom_left'][0] / divide
    stage_bottom = problem['stage_bottom_left'][1] / divide
    
    
    screen = pygame.display.set_mode([width, height])
    
    screen.fill((255, 255, 255))
    
    x, y = get_coordinates(stage_left, stage_bottom + stage_height, height)
    stage = pygame.Rect((x, y), (stage_width, stage_height))
    pygame.draw.rect(screen, (0, 0, 0), stage)
    
    for attende in problem['attendees']:
        x, y = get_coordinates(attende['x'] / divide, attende['y'] / divide, height)
        pygame.draw.circle(screen, (0, 255, 0, 1), (x, y), 5)
    
    pygame.display.update()
    
    while True:
        pass



if __name__ == '__main__':
    api = API(API_TOKEN)
    # visualize({
    #     "room_width": 2000.0,
    #     "room_height": 5000.0,
    #     "stage_width": 1000.0,
    #     "stage_height": 200.0,
    #     "stage_bottom_left": [500.0, 0.0],
    #     "musicians": [0, 1, 0],
    #     "attendees": [
    #         {"x": 100.0, "y": 500.0, "tastes": [1000.0, -1000.0]},
    #         {"x": 200.0, "y": 1000.0, "tastes": [200.0, 200.0]},
    #         {"x": 1100.0, "y": 800.0, "tastes": [800.0, 1500.0]}
    #     ]
    # })
    visualize(api.get_problem(1))
