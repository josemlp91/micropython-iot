import picoweb	
from setup import *

app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Hello world from picoweb running on the ESP32")

run_wifi_access_point()
app.run(debug=True, host = "192.168.4.1")