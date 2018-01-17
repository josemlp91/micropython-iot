import upip
import wifi
import ujson as json

def install_libs():

	wifi.connect()

	try:
		with open("/requirements.json") as f:
			requirements = json.loads(f.read())
	except (OSError, ValueError):
		print("Couldn't load /requirements.json")
    
	for requirement in requirements:
		upip.install(requirement)

		