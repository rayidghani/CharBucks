# runs the web app on a random port between 5000-5999, and opens the local browser

from app import app
import random, threading, webbrowser

port = 5000 + random.randint(0, 999)
url = "http://127.0.0.1:{0}".format(port)

threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

app.run(port=port, debug=False)
