import config
import wifi
import random
import time
from umqtt_broker import UmqttBroker

if __name__ == '__main__':
	
	wifi.connect()

	# Test subscribete Broker 
	#broker = UmqttBroker("led1")
	#broker.listen()

	# Test publish with broker
	broker = UmqttBroker("random")
	while True:
		broker.emit(random.randint(0, 9))
		time.sleep(5)