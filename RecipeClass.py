class RecipeClass:
    def __init__(self, data):
        self.ID =data['ID']
        self.ClassJobID =data['ClassJobID']
        self.Level =data['Level']
    
    def printObject(self):
        print(f"ID: {self.ID}")
        print(f"ClssJobId {self.ClassJobID}")
        print(f"Level {self.Level}")