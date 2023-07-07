from api import API
from config import API_TOKEN


class Solver():
    def __init__(self, api: API):
        self.api = api
    
    def solve(self, data: dict):
        return {}
    
    def solve_problem(self, id: int):
        problem = self.api.get_problem(id)
        
        data = self.solve(problem)
        
        return self.api.submit(id, data)
    
    def solve_all(self):
        amount = self.api.get_promblems_count()
        
        for i in range(1, amount + 1):
            submission = self.solve_problem(i)
            print(f'Problem {i} solved.')


if __name__ == '__main__':
    api = API(API_TOKEN)
    solver = Solver(api)
    
    solver.solve_all()
