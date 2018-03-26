from umqtt.simple import MQTTClient
import config as CONFIG
from machine import Pin
import machine
import ubinascii


class UmqttBroker(object):
	"""UmqttBroker"""
	
	def __init__(self):

		config = CONFIG.load_config()

		try:
			self.client_id = config["mqtt"]["client_id"]
			self.broker = config["mqtt"]["broker"]
			self.user = config["mqtt"]["user"]
			self.password = config["mqtt"]["password"]
			self.port = config["mqtt"]["port"]

		except:
			print("Couldn't load mqtt config param (client_id, broker url, user, password, port) in config.json")

		#Create an instance of MQTTClient 
		self.client = MQTTClient(self.client_id, self.broker, user=self.user, password=self.password, port=self.port)


	@staticmethod
	def onMessage(topic, msg):
		# Generic callback.
		print("Topic: %s, Message: %s" % (topic, msg))		
	

	def listen(self, topic):
		# Attach call back handler to be called on receiving messages
		self.client.set_callback(self.onMessage)
		self.client.connect()
		self.client.subscribe(topic)

		print("ESP8266 is Connected to %s and subscribed to %s topic" % (self.broker, topic))
	 
		try:
			while True:
				self.client.wait_msg()
		finally:
			self.client.disconnect()


	def emit(self, data, topic):
		self.client.connect()
		self.client.publish('{}'.format(topic),bytes(str(data), 'utf-8'))
		print('Sensor state: {}'.format(data))

	





		
		