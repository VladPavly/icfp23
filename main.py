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
        for _ in range(0,10):
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
            array[max_y - (stage[1] + 10)][max_x - (stage[0] + 10)] = 0


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
    stage_width = problem['stage_width']
    stage_height = problem['stage_height']
    stage_bottom_left = problem['stage_bottom_left']
    musicians = problem['musicians']

    dict_to_attende = lambda dict: Attendee(dict['x'], dict['y'], dict['tastes'])
    attendies = list(map(dict_to_attende, problem['attendees']))

    instruments = [Instruments() for _ in range(max(musicians) + 1)]

    for i in range(len(instruments)):
        array = [[0.0] * (stage_width - 20) for _ in range(stage_height - 20)]
        
        for attend in attendies:
            attend.find_impact(array, i, stage_bottom_left)
        
        instruments[i].find_coordinates(array)
        
        print(str(len(instruments[i].coordinates)), str(i))
        for coordinate in instruments[i].coordinates:
            coordinate.print()
