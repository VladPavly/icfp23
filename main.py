from api import API
from config import API_TOKEN
import sys
from visualisator import RewindClient
import math


class Coordinate():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self):
        return ' '.join([str(self.x), str(self.y), str(self.value)])

    def get_value(self):
        return self.value


class Instruments():
    def __init__(self):
        self.coordinates: list[Coordinate] = []
        self.empty = True
    
    def find_coordinates(self, instrument: int, attendies: list, size_y: int, size_x: int, stage: list[float], stage_points: dict[int, dict[int, Coordinate]]):
        zero = 0
      
        while len(self.coordinates) == 0:
            walls = [Coordinate(0, 0, float('-inf')) for _ in range(4)]
            
            for i in range(zero, size_y):
                x, y = zero + stage[0] + 10, i + stage[1] + 10
                count = find_impact(attendies, x, y, instrument)
                if count >= walls[0].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[0].value = count
                    walls[0].x = x
                    walls[0].y = y
                    
                debug(x, y) 
                   
                x, y = size_x + stage[0] + 10, i + stage[1] + 10
                count = find_impact(attendies, x, y, instrument)
                if count >= walls[1].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[1].value = count
                    walls[1].x = x
                    walls[1].y = y
                    
                debug(x, y) 

            for j in range(zero, size_x):
                x, y = j + stage[0] + 10, zero + stage[1] + 10
                count = find_impact(attendies, x, y, instrument)
                
                if count >= walls[2].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[2].value = count
                    walls[2].x = x
                    walls[2].y = y
                    
                debug(x, y)
                
                x, y = j + stage[0] + 10, size_y + stage[1] + 10
                count = find_impact(attendies, x, y, instrument)
                
                if count >= walls[3].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[3].value = count
                    walls[3].x = x
                    walls[3].y = y
                    
                debug(x, y)
            
            walls.sort(key = Coordinate.get_value)
            
            if walls[0].value > float('-inf') and (int(walls[0].x) not in stage_points or int(walls[0].y) not in stage_points[int(walls[0].x)] or stage_points[int(walls[0].x)][int(walls[0].y)].empty):
                self.coordinates.append(walls[0])
            else:
                zero += 11
                size_x -= 11
                size_y -= 11


class Attendee():
    def __init__(self, x, y, tastes):
        self.x = x
        self.y = y
        self.tastes = tastes


def find_impact(attendies: list[Attendee], x: int, y: int, instrument: int):
    count = 0
    
    for attende in attendies:
        distance = math.sqrt((attende.x - x) ** 2 + (attende.y - y) ** 2)
        count += math.ceil(10000000 * attende.tastes[instrument] / distance ** 2) if distance != 0 else 0
    
    return count


def debug(x: int, y: int):
    client.circle(x / divide, y / divide, 1, client.GREEN, True)  


def main(problem: dict):
    global client, divide
    
    print('Preparing...', file=sys.stderr)
    
    stage_width: int = problem['stage_width']
    stage_height: int = problem['stage_height']
    stage_bottom_left: list[int] = problem['stage_bottom_left']
    musicians: list = problem['musicians']

    dict_to_attende = lambda dict: Attendee(dict['x'], dict['y'], dict['tastes'])
    attendies = list(map(dict_to_attende, problem['attendees']))
    
    client = RewindClient()
    divide = 2
    
    for attende in attendies:
        client.circle(attende.x / divide, attende.y / divide, 5, client.BLUE, True)

    instruments = [Instruments() for _ in range(max(musicians) + 1)]
    
    print('Starting script...', file=sys.stderr)
    
    result = {
        'placements': [{'x': None, 'y': None} for _ in range(len(musicians))]
    }
    
    stage_points = {}
    score = 0
    
    client.rectangle(stage_bottom_left[0] / divide, (stage_bottom_left[1] + stage_height) / divide, (stage_bottom_left[0] + stage_width) / divide, stage_bottom_left[1] / divide, 0, False)

    for i in range(len(instruments)):
        for _ in range(musicians.count(i)):
            instruments[i].find_coordinates(i, attendies, int(stage_height - 20), int(stage_width - 20), stage_bottom_left, stage_points)
            coordinate = instruments[i].coordinates[0]

            coordinate.empty = False
            score += coordinate.value
            
            client.circle(coordinate.x / divide, coordinate.y / divide, 5, client.RED, True)  
            
            for ax in range(-10, 11):
                for ay in range(-10, 11):
                    if (ax / 10) ** 2 + (ay / 10) ** 2 <= 1:
                        if int(coordinate.x + ax) not in stage_points:
                            stage_points[int(coordinate.x + ax)] = {}
                        
                        stage_points[int(coordinate.x + ax)][int(coordinate.y + ay)] = coordinate
            
            musician_id = musicians.index(i)
            
            result['placements'][musician_id]['x'] = coordinate.x
            result['placements'][musician_id]['y'] = coordinate.y
            print(f'Musician {musician_id} - {coordinate.x} {coordinate.y} {round(coordinate.value, 2)}', file=sys.stderr)
            
            musicians[musician_id] = -1
            instruments[i].coordinates = []
    
    print(f'Score - {score}', file=sys.stderr)
    client.end_frame()
    
    return result


if __name__ == '__main__':
    api = API(API_TOKEN)
    main({
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
    # main(api.get_problem(1))
