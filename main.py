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
    
    def find_coordinates(self, instrument, Attendies, sizey, sizex, stage: list[float], stage_points: dict[int, dict[int, Coordinate]]):
        max_value = float('-inf')
        max_x = 0
        max_y = 0
        zerox = 0
        zeroy = 0
        while len(self.coordinates) == 0:
            Walls = [Coordinate(0,0,float('-inf')) for _ in range(4)]
            for i in range(zeroy,sizey):
                x, y = zerox + stage[0] + 10, i + stage[1] + 10
                count = find_impact(Attendies, y, x, instrument)
                if count >= Walls[0].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    Walls[0].value = count
                    Walls[0].x = x
                    Walls[0].y = y
                x, y = sizex + stage[0] + 10, i + stage[1] + 10
                count = find_impact(Attendies, y, x, instrument)
                if count >= Walls[1].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    Walls[1].value = count
                    Walls[1].x = x
                    Walls[1].y = y

            for j in range(zerox, sizex):
                x, y = j + stage[0] + 10, zeroy + stage[1] + 10
                count = find_impact(Attendies, y, x, instrument)
                if count >= Walls[2].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    Walls[2].value = count
                    Walls[2].x = x
                    Walls[2].y = y
                x, y = j + stage[0] + 10, sizey + stage[1] + 10
                count = find_impact(Attendies, y, x, instrument)
                if count >= Walls[3].value and (int(x) not in stage_points or int(y) not in stage_points[int(x)] or stage_points[int(x)][int(y)].empty):
                    Walls[3].value = count
                    Walls[3].x = x
                    Walls[3].y = y
            
            Walls.sort(key = Coordinate.ret_value)
            if Walls[0].value > float('-inf') and (int(Walls[0].x) not in stage_points or int(Walls[0].y) not in stage_points[int(Walls[0].x)] or stage_points[int(Walls[0].x)][int(Walls[0].y)].empty):
                self.coordinates.append(Walls[0])
            else:
                zerox+=11
                zeroy+=11
                sizex-=10
                sizey-=10


class Attendee():
    def __init__(self, x, y, tastes):
        self.x = x
        self.y = y
        self.tastes = tastes

def find_impact(Attendies, i, j, instrument):
    count = 0
    for att in Attendies:
        count += 10000000 * att.tastes[instrument] / abs(
            pow(att.x - j, 2) + pow(att.y - i, 2)
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
        # array = [[0.0] * int(stage_width - 20) for _ in range(int(stage_height - 20))]
        
        # find_impact(attendies, array, i, stage_bottom_left)
        
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
