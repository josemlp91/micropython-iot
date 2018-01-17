from config import load_config
import network

def connect():
    """
    Conectar placa micropython a la red WIFI.
    """

    config = load_config()

    try:
        ssid = config["wifi"]["ssid"]
        password = config["wifi"]["password"]
    except:
        print("Couldn't load wifi ssid and password from config.json")

    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        return
 
    station.active(True)
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass

