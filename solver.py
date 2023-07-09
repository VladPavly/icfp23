from api import API
from config import API_TOKEN
from visualisator import FakeClient
from main import main
import sys
from multiprocessing import Process, freeze_support


class Solver():
    def __init__(self, api: API):
        self.api = api
    
    def solve(self, data: dict):
        global client
        
        client = FakeClient()
        
        return main(data)
    
    def solve_problem(self, id: int):
        problem = self.api.get_problem(id)
        
        data = self.solve(problem)
        
        print(f'Problem {id} solved.', file=sys.stderr)
        return self.api.submit(id, data)
    
    def solve_all(self):
        amount = self.api.get_promblems_count()
        
        processes: list[Process] = []
        for i in range(1, amount + 1):
            processes.append(Process(target=self.solve_problem, args=(i,)))
        
        for process in processes:
            process.start()


if __name__ == '__main__':
    freeze_support()
    
    api = API(API_TOKEN)
    solver = Solver(api)
    
    solver.solve_all()
