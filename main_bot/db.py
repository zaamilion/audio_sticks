import json
import functions
class Database:
    def __init__(self, file_name):
        self.file_name = file_name
        self.list = {}
    def dump(self):
        with open(f'{self.file_name}.json', 'w') as file:
            dumping = {}
            for key, value in self.list.items():
                dumping[key] = [value[0].to_dict(), value[1]]
            json.dump(dumping, file)
    def load(self):
        with open(f'{self.file_name}.json', 'r') as file:
            self.list = json.load(file)
            for user, value in self.list.items():
                self.list[user][0] = functions.to_classs(value[0])
            
            return self.list