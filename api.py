import httpx
from config import API_TOKEN
import json


class API():
    def __init__(self, token: str, url: str = 'https://api.icfpcontest.com/'):
        self.url = url
        self.token = token
    
    def parse(self, data: dict):
        if 'Success' in data:
            return json.loads(data['Success'])
        else:
            print(data['Failure'])
            raise Exception('API exception')
    
    def get_problem(self, id: int):
        problem = self.parse(httpx.get(self.url + f'problem?problem_id={id}', headers={'Authorization': f'Bearer {self.token}'}).json())
        
        return problem
    
    def get_promblems_count(self):
        count = httpx.get(self.url + f'problems', headers={'Authorization': f'Bearer {self.token}'}).json()['number_of_problems']
        
        return count
    
    def submit(self, id: int, data: dict):
        submission_id = str(httpx.post(self.url + f'submission', headers={'Authorization': f'Bearer {self.token}'},
                                 json={
                                        'problem_id': id,
                                        'contents': json.dumps(data)
                                     }
        ).text)
        
        return self.get_submission(submission_id[1:-1])
    
    def get_submission(self, id: str):
        submission = httpx.get(self.url + f'submission?submission_id={id}', headers={'Authorization': f'Bearer {self.token}'}).json()['Success']
        
        return submission


if __name__ == '__main__':
    api = API(API_TOKEN)
    print(api.submit(1, {'hello': 'world'}))
