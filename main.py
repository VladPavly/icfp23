from api import API
from config import API_TOKEN


class Coordinate():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def print(self):
        print(str(self.x), str(self.y), str(self.value))


class Instruments():
    def __init__(self):
        self.coordinates: list[Coordinate] = []
    
    def find_coordinates(self, array, stage: list[float]):
        max_value = float('-inf')
        max_x = 0
        max_y = 0
        for _ in range(0, 10):
            i = 0
            while i < len(array):
                j = 0
                
                while j < len(array[i]):
                    if array[i][j] >= max_value:
                        max_value = array[i][j]
                        max_x = j + stage[0] + 10
                        max_y = i + stage[1] + 10
                    
                    j += 1
                
                i += 1
            
            self.coordinates.append(Coordinate(max_x, max_y, max_value))
            max_value = 0
            array[round(max_y - (stage[1] + 10))][round(max_x - (stage[0] + 10))] = 0


class Attendee():
    def __init__(self, x, y, tastes):
        self.x = x
        self.y = y
        self.tastes = tastes

    def find_impact(self, array, instrument, bottom_left):
        i = 0
        j = 0
        
        while i < len(array):
            j = 0
            
            while j < len(array[i]):
                array[i][j] += 10000000 * self.tastes[instrument] / abs(
                    pow(self.x - (j + bottom_left[0] + 10), 2) + pow(self.y - (i + bottom_left[1] + 10), 2)
                )
                j += 1
                
            i += 1


def main(problem: dict):
    print('Preparing...')
    
    stage_width = problem['stage_width']
    stage_height = problem['stage_height']
    stage_bottom_left = problem['stage_bottom_left']
    musicians = problem['musicians']

    dict_to_attende = lambda dict: Attendee(dict['x'], dict['y'], dict['tastes'])
    attendies = list(map(dict_to_attende, problem['attendees']))
    attendies_count = len(attendies)

    instruments = [Instruments() for _ in range(max(musicians) + 1)]
    
    print('Starting script...')

    for i in range(len(instruments)):
        array = [[0.0] * round(stage_width - 20) for _ in range(round(stage_height - 20))]
        
        a = 0
        for attend in attendies:
            attend.find_impact(array, i, stage_bottom_left)
            a += 1
            print(f'Instrument {i} - {a / attendies_count * 100}%')
        
        instruments[i].find_coordinates(array, stage_bottom_left)
        
        print(str(len(instruments[i].coordinates)), str(i))
        for coordinate in instruments[i].coordinates:
            coordinate.print()


if __name__ == '__main__':
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
