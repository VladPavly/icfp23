from api import API
from config import API_TOKEN
import sys


class Coordinate():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def print(self):
        print(str(self.x), str(self.y), str(self.value))

    def ret_value(self):
        return self.value


class Instruments():
    def __init__(self):
        self.coordinates: list[Coordinate] = []
        self.empty = True
    
    def find_coordinates(self, instrument, attendies, size_y, size_x, stage: list[float], stage_points: dict[int, dict[int, Coordinate]]):
        zero_x = 0
        zero_y = 0
        
        while len(self.coordinates) == 0:
            walls = [Coordinate(0, 0, float('-inf')) for _ in range(4)]
            
            for i in range(zero_y, size_y):
                x, y = zero_x + stage[0] + 10, i + stage[1] + 10
                count = find_impact(attendies, y, x, instrument)
                if count >= walls[0].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[0].value = count
                    walls[0].x = x
                    walls[0].y = y
                
                x, y = size_x + stage[0] + 10, i + stage[1] + 10
                count = find_impact(attendies, y, x, instrument)
                if count >= walls[1].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[1].value = count
                    walls[1].x = x
                    walls[1].y = y

            for j in range(zero_x, size_x):
                x, y = j + stage[0] + 10, zero_y + stage[1] + 10
                count = find_impact(attendies, y, x, instrument)
                if count >= walls[2].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[2].value = count
                    walls[2].x = x
                    walls[2].y = y
                
                x, y = j + stage[0] + 10, size_y + stage[1] + 10
                count = find_impact(attendies, y, x, instrument)
                
                if count >= walls[3].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    walls[3].value = count
                    walls[3].x = x
                    walls[3].y = y
            
            walls.sort(key = Coordinate.ret_value)
            if walls[0].value > float('-inf') and (int(walls[0].x) not in stage_points or int(walls[0].y) not in stage_points[int(walls[0].x)] or stage_points[int(walls[0].x)][int(walls[0].y)].empty):
                self.coordinates.append(walls[0])
            else:
                zero_x += 11
                zero_y += 11
                size_x -= 10
                size_y -= 10


class Attendee():
    def __init__(self, x, y, tastes):
        self.x = x
        self.y = y
        self.tastes = tastes

def find_impact(attendies, i, j, instrument):
    count = 0
    
    for attende in attendies:
        count += 10000000 * attende.tastes[instrument] / abs(
            (attende.x - j) ** 2 + (attende.y - i) ** 2
        )
    
    return count

def main(problem: dict):
    print('Preparing...', file=sys.stderr)
    
    stage_width: int = problem['stage_width']
    stage_height: int = problem['stage_height']
    stage_bottom_left: list[int] = problem['stage_bottom_left']
    musicians: list = problem['musicians']

    dict_to_attende = lambda dict: Attendee(dict['x'], dict['y'], dict['tastes'])
    attendies = list(map(dict_to_attende, problem['attendees']))

    instruments = [Instruments() for _ in range(max(musicians) + 1)]
    
    print('Starting script...', file=sys.stderr)
    
    result = {
        'placements': [{'x': None, 'y': None} for _ in range(len(musicians))]
    }
    
    stage_points = {}
    score = 0

    for i in range(len(instruments)):
        for _ in range(musicians.count(i)):
            instruments[i].find_coordinates(i, attendies, int(stage_width - 20),int(stage_height - 20), stage_bottom_left, stage_points)
            coordinate = instruments[i].coordinates[0]

            coordinate.empty = False
            score += coordinate.value
            
            
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
    
    return result


if __name__ == '__main__':
    ap = API(API_TOKEN)
    main(ap.get_problem(id=1))
