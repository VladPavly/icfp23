from api import API
from config import API_TOKEN
import sys
from visualisator import RewindClient, FakeClient
import math
import json


class Coordinate():
    def __init__(self, x, y, value = float('-inf')):
        self.x = x
        self.y = y
        self.value = value
        self.empty = True

    def __repr__(self):
        return f'Coordinate(x={self.x}, y={self.y}, value={self.value})'
    
    def distance(self, coordinate):
        distance = math.sqrt((self.x - coordinate.x) ** 2 + (self.y - coordinate.y) ** 2)
        
        return distance
    
    def to_vector(self):
        return (self.x, self.y)
    
    def obstacle(self, coordinate):
        vectors = [self.to_vector(), coordinate.to_vector()]
        
        for obstacle in obstacles:
            if circle_line_segment_intersection(*obstacle, *vectors):
                return True
        
        return False


class Instrument():
    def __init__(self):
        self.empty = True
        self.musicians = []
    
    def find_coordinates(self, instrument: int, attendees: list, size_y: int, size_x: int, stage: list[float], stage_points: dict[int, dict[int, Coordinate]]) -> Coordinate:
        zero = 0
        best = Coordinate(0, 0)
      
        while True:
            walls = [Coordinate(0, 0) for _ in range(4)]
            changed = False
            
            # for i in range(size_x):
            #     for j in range(size_y):
            #         x, y = i + stage[0] + 10, j + stage[1] + 10
            #         count = find_impact(attendees, x, y, instrument)
                    
            #         if count >= walls[0].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
            #             idx = int(i + j * size_x)
            #             walls[idx].value = count
            #             walls[idx].x = x
            #             walls[idx].y = y
                    
            
            for i in range(zero, size_y):
                x, y = zero + stage[0] + 10, i + stage[1] + 10
                count = find_impact(attendees, Coordinate(x, y), instrument)
                
                if count >= walls[0].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[0].value = count
                    walls[0].x = x
                    walls[0].y = y
                    
                debug(x, y) 
                   
                x, y = size_x + stage[0] + 10, i + stage[1] + 10
                count = find_impact(attendees, Coordinate(x, y), instrument)
                
                if count >= walls[1].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[1].value = count
                    walls[1].x = x
                    walls[1].y = y
                    
                debug(x, y) 

            for j in range(zero, size_x):
                x, y = j + stage[0] + 10, zero + stage[1] + 10
                count = find_impact(attendees, Coordinate(x, y), instrument)
                
                if count >= walls[2].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[2].value = count
                    walls[2].x = x
                    walls[2].y = y
                    
                debug(x, y)
                
                x, y = j + stage[0] + 10, size_y + stage[1] + 10
                count = find_impact(attendees, Coordinate(x, y), instrument)
                
                if count >= walls[3].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[3].value = count
                    walls[3].x = x
                    walls[3].y = y
                    
                debug(x, y)
            
            walls.sort(key = lambda coordinate: coordinate.value, reverse = True)
            
            
            if walls[0].value > best.value and (int(walls[0].x) not in stage_points or int(walls[0].y) not in stage_points[int(walls[0].x)] or stage_points[int(walls[0].x)][int(walls[0].y)].empty):
                best = walls[0]
                changed = True
            
            if best.value == float('-inf') or changed:
                zero += 10
                size_x -= 10
                size_y -= 10
            else:
                break
        
        return best


class Attendee():
    def __init__(self, x, y, tastes):
        self.position = Coordinate(x, y)
        self.tastes = tastes


def find_impact(attendees: list[Attendee], coordinate: Coordinate, instrument: int):
    count = 0
    
    for attendee in attendees:
        if not attendee.position.obstacle(coordinate):
            distance = attendee.position.distance(coordinate)
            count += max(math.ceil(1_000_000 * attendee.tastes[instrument] / (distance ** 2)) if distance != 0 else 0, 0)
    
    return count


def circle_line_segment_intersection(circle_center, circle_radius, point_1, point_2):
    (p1x, p1y), (p2x, p2y), (cx, cy) = point_1, point_2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** 0.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:
        return False
    else:
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant ** 0.5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant ** 0.5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]
        
        fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
        intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        
        if len(intersections) == 2 and abs(discriminant) <= 1e-9:
            return False
        else:
            return True


def debug(x: int, y: int):
    # client.circle(x / divide, y / divide, 1, client.GREEN, True)  
    pass


def main(problem: dict):
    global client, divide, obstacles
    
    print('Preparing...', file=sys.stderr)
    
    stage_width: int = problem['stage_width']
    stage_height: int = problem['stage_height']
    stage_bottom_left: list[int] = problem['stage_bottom_left']
    musicians: list = problem['musicians']
    musicians_parsed = 0

    dict_to_attendee = lambda dict: Attendee(dict['x'], dict['y'], dict['tastes'])
    attendees = list(map(dict_to_attendee, problem['attendees']))
    
    divide = 50
    
    obstacles = []
    if 'pillars' in problem:
        pillar_parser = lambda pillar: (tuple(pillar['center']), pillar['radius'])
        obstacles = list(map(pillar_parser, problem['pillars']))
    
    print(f'Pillars - {len(obstacles)}')
    
    for pillar in obstacles:
        client.circle(pillar[0][0] / divide, pillar[0][1] / divide, pillar[1] / divide, client.DARK_GREEN, True)
    
    for attendee in attendees:
        client.circle(attendee.position.x / divide, attendee.position.y / divide, 5 / divide, client.BLUE, True)

    instruments = [Instrument() for _ in range(max(musicians) + 1)]
    
    print('Starting script...', file=sys.stderr)
    
    result = {
        'placements': [{'x': None, 'y': None} for _ in range(len(musicians))],
        'volumes': [1 for _ in range(len(musicians))]
    }
    
    stage_points = {}
    score = 0
    
    client.rectangle(stage_bottom_left[0] / divide, (stage_bottom_left[1] + stage_height) / divide, (stage_bottom_left[0] + stage_width) / divide, stage_bottom_left[1] / divide, 0, False)
    
    # client.end_frame() # Enable this if you wanna see problem

    for i in range(len(instruments)):
        for _ in range(musicians.count(i)):
            coordinate = instruments[i].find_coordinates(i, attendees, int(stage_height - 20), int(stage_width - 20), stage_bottom_left, stage_points)
            obstacles.append([coordinate.to_vector(), 5])

            coordinate.empty = False
            score += coordinate.value
            
            if coordinate.value > 0:
                volume = 10
            else:
                volume = 0
            
            client.circle(coordinate.x / divide, coordinate.y / divide, 5 / divide, client.RED, True)
            
            for ax in range(-10, 11):
                for ay in range(-10, 11):
                    if (ax / 10) ** 2 + (ay / 10) ** 2 <= 1:
                        if int(coordinate.x + ax) not in stage_points:
                            stage_points[int(coordinate.x + ax)] = {}
                        
                        stage_points[int(coordinate.x + ax)][int(coordinate.y + ay)] = coordinate
            
            musician_id = musicians.index(i)
            
            result['placements'][musician_id]['x'] = coordinate.x
            result['placements'][musician_id]['y'] = coordinate.y
            result['volumes'][musician_id] = volume
            
            musicians_parsed += 1
            print(f'Musician {musicians_parsed}/{len(musicians)} ({musician_id}) - {coordinate.x} {coordinate.y} {coordinate.value * volume}', file=sys.stderr)
            
            musicians[musician_id] = -1
    
    print(f'Score - {score}', file=sys.stderr)
    client.end_frame()
    
    return result


if __name__ == '__main__':
    api = API(API_TOKEN)
    
    if input('Use visualisator (y/N): ').lower().startswith('y'):
        client = RewindClient()
    else:
        client = FakeClient()
    
    if input('Use sample (Y/n): ').lower().startswith('n'):
        result = main(api.get_problem(int(input('Problem number: '))))
    else:
        result = main({
            "room_width": 2000.0,
            "room_height": 5000.0,
            "stage_width": 1000.0,
            "stage_height": 200.0,
            "stage_bottom_left": [500.0, 0.0],
            "musicians": [0, 1, 0],
            "attendees": [
                {"x": 100.0, "y": 500.0, "tastes": [1000.0, -1000.0]},
                {"x": 200.0, "y": 1000.0, "tastes": [200.0, 200.0]},
                {"x": 1100.0, "y": 800.0, "tastes": [800.0, 1500.0]}
            ]
        })
    
    print(json.dumps(result))
