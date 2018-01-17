from umqtt.simple import MQTTClient
import config as CONFIG
from machine import Pin
import machine
import ubinascii



class UmqttBroker(object):
	"""docstring for UmqttBroker"""
	
	def __init__(self, topic):

		config = CONFIG.load_config()

		try:
			self.client_id = config["mqtt"]["client_id"]
			self.broker = config["mqtt"]["broker"]
			self.user = config["mqtt"]["user"]
			self.password = config["mqtt"]["password"]
			self.port = config["mqtt"]["port"]

		except:
			print("Couldn't load mqtt config param (client_id, broker url, user, password, port) in config.json")

		try:
			self.topic = config["mqtt"]["topics"][topic]
		except:
			print("Don't exits the topic %s in config.json topic") % (topic)

		
		#Create an instance of MQTTClient 
		self.client = MQTTClient(self.client_id, self.broker, user=self.user, password=self.password, port=self.port)


	def listen(self):
		# Attach call back handler to be called on receiving messages
		self.client.set_callback(onMessage)
		self.client.connect()
		self.client.subscribe(self.topic)

		print("ESP8266 is Connected to %s and subscribed to %s topic" % (self.broker,self.topic))
	 
		try:
			while True:
				self.client.wait_msg()
		finally:
			self.client.disconnect()

	def emit(self, data):
		self.client.connect()
		self.client.publish('{}'.format(self.topic),bytes(str(data), 'utf-8'))
		print('Sensor state: {}'.format(data))


#################################################################################
# CUSTOM CALLBACK

bulbPin = Pin(22, Pin.OUT)

def onMessage(topic, msg):

	print("Topic: %s, Message: %s" % (topic, msg))
 
	if msg == b"1":
		bulbPin.value(1)
	elif msg == b"0":
		bulbPin.value(0)

		
		