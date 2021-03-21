
class ATM():
    """ ATM information """
    def __init__(self,name: str,address: str,dist:float):
        self.name = name
        self.address = address
        self.current_distance = dist