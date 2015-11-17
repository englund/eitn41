import random
class client:
    def __init__(self,id):
        self.id = id
    
    def create_message(self):
        return random.randint(1,1000)

class message:
    def __init__(self, message, sender, receiver):
        self.message = message
        self.sender = sender
        self.receiver = receiver
class mix:
    def __init__(self,id):
        self.id = id

    def insert(self, message):
        pass
    

if __name__ == "__main__":
    c1 = client(1)
    m = mix(1)

