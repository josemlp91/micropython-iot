# Micropython y MQTT.

[TOC]

## ¿Que es Micropython ?

Micropython es un pequeño pero eficiente interprete de [Python 3](https://www.python.org/) que incluye un subconjunto mínimo de librerías y que se encuentra optimizado para que pueda correr en microcontroladores y ambientes restringidos.

### Características

- Cuenta con una consola interactiva.
- Muchas librerías, que se pueden instalar usando **upip**.



### ¿Donde ejecutar Micropython?

Micropython se puede instalar en la mayoría de los sistema operativos **UNIX**, pero lo interesante es instalarlo en alguna de los microcontroladores que lo soportan.

-  [Pyboard](https://www.adafruit.com/product/2390)
-  [WiPy](https://www.adafruit.com/product/3184)
-  [ESP8266](https://www.adafruit.com/product/2821)
-  [ESP32](https://en.wikipedia.org/wiki/ESP32)



Estos microcontroladores tienen una potencia limitada, pero con la ventaja de incorporar conexión wifi, un consumo energético bastante bajo y un precio muy bajo, (menos de 10$). Además son fácilmente flasheables con **micropython**.

## Requisitos

Debes tener instalado **Python** y el gestor de paquetes **pip** y consola serie ``sudo apt-get install minicom``

1. Instalar utilidades para poder flashear la tarjeta.

  ```bash
  pip install esptool
  ```

2.  Instalar herramientas para interactuar con la placa.

   ```bash
   pip install adafruit-ampy
   ```

## Instalación

1. Descargar última versión de micropython soportada por tu tarjeta.

  **ESP32**

  ```bash
  wget http://micropython.org/resources/firmware/esp32-20180412-v1.9.3-548-gd12483d9.bin
  ```

  **ESP8266**

  ```bash
  wget http://micropython.org/resources/firmware/esp8266-20170823-v1.9.2.bin
  ```

2. Conecta tu placa mediante conexión **usb** a tu ordenador.

3. Localiza la ruta del usb que acabas de conectar (en linux ejecuta lo siguiente.

  ```bash
  ls /dev/ttyUSB*
  ```

4. Borrar la memoria flash actual de nuestro micro

   ```bash
   esptool.py --port /dev/ttyUSB0 erase_flash
   ```

5. Instalar micropython.

   **ESP32**

   ```bash
   esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 ./esp32-20180412-v1.9.3-548-gd12483d9.bin
   ```

   **ESP8266**

   ```bash
   esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect -fm dio 0 ./esp8266-20170823-v1.9.2.bin
   ```


7. Iniciar consola serie para comunicar comandos a la placa micropython.

   ```bash
   minicom --baudrate 115200 --device /dev/ttyUSB0
   ```

   ```bash
   Welcome to minicom 2.7

   OPCIONES: I18n 
   Compilado en Feb  7 2016, 13:37:27.
   Port /dev/ttyUSB0, 16:35:20

   Presione CTRL-A Z para obtener ayuda sobre teclas especiales

   >>> print("hello world")
   hello world

   >>> import machine
   >>> led = machine.Pin(22, machine.Pin.OUT)
   >>> led.value(1)

   ```
   Como vemos ya tenemos un interprete Python.


8. Subir código fuente, ejemplo ``main.py``.

   ```python
   print("hello world")
   ```

    ```bash
   ampy --port /dev/ttyUSB0 put ./main.py
    ```

   ```bash
   ampy --port /dev/ttyUSB0 ls

   boot.py
   main.py
   ```


## ¿Que es MQTT?

[MQTT](http://mqtt.org/) son las siglas de **Message Queue Telemetry Transport** y tras ellas se encuentra un protocolo ideado por **IBM** y liberado para que cualquiera podamos usarlo enfocado a la **conectividad Machine-to-Machine (M2M)** .

**MQTT** sigue una topología en estrella**, donde existe un **nodo central o **broker** tiene capacidad para trabajar con un gran número de clientes y gestionar la conectividad entre ellos. Y la comunicación puede ser de uno a uno o de uno a muchos.

También proporciona la capa de seguridad, autenticación y cifrado necesaria.

Para el enrrutamiento de los mensajes se usa el concepto **topic** o tema,  el topic es una etiqueta para diferencias los diferentes mensajes mqtt que circulan la red y pueden tener una forma jerárquica.

**Ejemplo:**

- casaplaya
- casaplaya/salon
- casaplaya/salon/luz1
- casaplaya/sensorprecensia
- casaplaya/sensortemperatura

Entorno al **topic** podemos realizar dos acciones **publicar** mensajes (*public*) o **subscribir** a los mensajes de un determinado tópico (*subscript*).

De esta forma un sensor, puede publicar un mensaje X cada N tiempo en un determinado tópico.

**Ejemplo:**

``Sensor de temperatura`` ``publica`` en tópico ``sensors/temperature`` mensaje con la temperatura ``T`` cada ``15 minutos``.

``Luz`` se ``subscribe`` a tópico ``light``  y espera mensajes ``ON`` o ``OFF`` dado los cuales se enciende o apaga.



## Integrar MQTT con Micropython

Y puestos en este punto se nos ocurre la forma de implementar una aplicación domótica usando estas tecnologías, quizá parezca complicado, pero te aseguro que es más simple de lo que parece.

El primer paso es tener un **broker MQTT** que gestione los mensajes, no es muy complejo hacer una instalación en un servidor propio, pero existen soluciones cloud mucho más simples de usar.

[CloudMQTT](https://www.cloudmqtt.com/) ofrece un plan gratuito de hasta 10 conexiones.  Para empezar debes registrarte y crear una **instancia**.

Una vez creado al consultar la configuración de la instancia veras algo parecido.



![](http://pix.toile-libre.org/upload/original/1523215094.png)



###Conectar Micropython a MQTT

Asumimos que se ha completado la instalación anterior.

1. Descargar repositorio: [micropython-iot](https://github.com/josemlp91/micropython-iot)

2. Modificar configuración, ``cp config.json.dev config.json`` y modificar la configuración para conectarte a la ``red wifi``, y al ``broker mqtt`` antes configurado.

   Ejemplo:

   ```json
   {
   	"wifi":{
   		"ssid":"XXXXX",
   		"password":"XXXXX"
   	},
   	"mqtt":{
   		"broker": "m14.cloudmqtt.com",
   		"user": "XXXX",
   		"password": "XXXXX",
   		"port": "19970",
   		"client_id": "esp8266_XXXXXX"
   	}   
   }
   ```

3. Actualizar código fuente a la placa  usando comando ``update.sh``

4. Acceder a consola mediante comando ``console.sh``

5. Instalar bibliotecas adicionales, desde ``upip``.

   ```python
   from install import *
   install_libs()
   ```

6. Ver código ``main.py``,  este es el código que se ejecuta al conectar el microcontrolador, automáticamente accede a la configuración wifi y mqtt y se subscribe a topic dado.

   Como podemos ver el callback asociado a los mensajes con el topic dado, se encarga de encender y apagar el LED del pin 22.

   ```python
   import config
   import wifi
   from umqtt_broker import UmqttBroker
   from machine import Pin

   class LedUmqttBroker(UmqttBroker):

   	@staticmethod
   	def onMessage(topic, msg):
   		"""Callback message topic"""
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

   ```

### Configurar cliente Android

1. Instalar aplicación desde la Play Store. **MQTT Dashboard**.
2. Añadir una nueva conexión y establecer la configuración dada en **Cloud MQTT**
3. Crear un nuevo control tipo **switch** subscrito al **topic**  **test/led** que pública los mensajes ``0`` y ``1``.

![](http://pix.toile-libre.org/upload/original/1523217187.png)

## Recursos

https://github.com/espressif/esptool

https://pagefault.blog/2017/03/02/using-local-mqtt-broker-for-cloud-and-interprocess-communication/


## Disclainer

Este proyecto se encuentra en fase de desarrollo como parte de un proyecto personal destinado al aprendizaje de las tecnologías involucradas, el autor no se responsabiliza de cualquier defecto del software. Úselo y modifíquelo bajo su propia responsabilidad. 


## Autor

- José M López Pérez [josmilopeREMOVETHIS@gmail.es](josmilopeREMOVETHIS@gmail.es)


