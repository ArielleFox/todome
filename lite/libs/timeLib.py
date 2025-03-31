import datetime


def get_current_time(switch: bool):
	if switch == False:
		now = datetime.datetime.now().strftime("%I:%M %p")
	elif switch == True:
		now = datetime.datetime.now().strftime("%H:%M")
	return now
if __name__ == '__main__':
	print(get_current_time(switch=True))
	print(get_current_time(switch=False))

