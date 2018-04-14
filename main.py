import config
import wifi
import time
from umqtt_broker import UmqttBroker
from machine import Pin

class LedUmqttBroker(UmqttBroker):

	@staticmethod
	def onMessage(topic, msg):
		
		PIN_N = 22
		ON_VALUE = b"1"
		OFF_VALUE = b"0"

		bulbPin = Pin(PIN_N, Pin.OUT)
		
		if msg == ON_VALUE:
			bulbPin.value(1)
		elif msg == OFF_VALUE:
			bulbPin.value(0)


if __name__ == '__main__':


	wifi.connect()

	# Test subscribete Broker 
	broker = LedUmqttBroker()
	broker.listen("test/led")
