
class ATM():
    """ ATM information """
    def __init__(self,name: str,address: str, lat:str,long:str,dist:float):
        self.name = name
        self.address = address
        self.lat = lat
        self.long = long
        self.current_distance = dist