
def findATMs():
	return "buscandoooooooo"


def getLocation(bot, update):
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    return (message.location.latitude, message.location.longitude)

def calculateDistance(p1,p2):
	earthR = 6373.0

	lat1 = math.radians(p1[0])
	lat2 = math.radians(p2[0])

	lon1 = math.radians(p1[1])
	lon2 = math.radians(p2[1])

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	#Haversine formula
	a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

	return earthR * c