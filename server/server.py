# Funicular.js - Websocket Server Component
# https://github.com/adeniszczyc/Funicular.js
#
# Ensure you have read the README and have all dependancies up and running.
# Run through terminal with:
# $ python server.py

#### ------- Config Settings ------- ####

port = 8888


#### ------- Imports ------- ####

# tornado - Websocket Communication with Browser
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback


# Threading
from threading import Thread
from Queue import Queue

# openni - Kinect Tracking
from openni import *

# Other utilities
import time
import random
import copy

#### ------- Kinect / OpenNI Communication ------- ####

q = Queue()
hands = {"hands": {}}

class kinect(Thread):

  def __init__(self):
    Thread.__init__(self)
    self.daemon = True
    self.active = True
    self.start()

  def run(self):

    self.context = Context()
    self.context.init()

    self.gesture_generator = GestureGenerator()
    self.gesture_generator.create(self.context)
    self.gesture_generator.add_gesture('Wave')
    self.gesture_generator.add_gesture('Click')

    self.hands_generator = HandsGenerator()
    self.hands_generator.create(self.context)
  
    def gesture_detected(src, gesture, id, end_point):

        self.hands_generator.start_tracking(end_point)

        q.put({"type": "gesture", "gesture": gesture, "end_point": end_point})
        if gesture == "Click":
          print "Gesture Detected: Click"

        elif gesture == "Wave":
            print "Gesture Detected: Wave"

    def gesture_progress(src, gesture, id, end_point):
        pass

    def create(src, id, pos, time):

        coordinates = {}
        coordinates["id"] = id
        coordinates["x"] = pos[0]
        coordinates["y"] = pos[1]
        coordinates["z"] = pos[2]

        q.put({"type": "register", "id": id, "x": pos[0], "y": pos[1], "z": pos[2]})

        print 'Detected hand, now tracking.'

    def update(src, id, pos, time):
      global hands
     
      coordinates = {}
      coordinates["id"] = id
      coordinates["x"] = pos[0]
      coordinates["y"] = pos[1]
      coordinates["z"] = pos[2]

      hands["hands"][id] = coordinates

    def destroy(src, id, time):
        global hands

        q.put({"type": "unregister", "id": id})
        
        try:
            del hands["hands"][id]
        except:
            pass

        print 'Lost hand tracking. Wave to restart tracking.'

      


    self.gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
    self.hands_generator.register_hand_cb(create, update, destroy)

    self.context.start_generating_all()

# Open up Kinect Thread
tracking = kinect()


#### ------- Websocket Connection ------- ####

class WSHandler(tornado.websocket.WebSocketHandler):

    # Websocket connection has opened with client.
    # Run loop every 5 milliseconds
    def open(self):
        self.callback = PeriodicCallback(self.loop, 5)
        self.callback.start()

        global hands
        self.lastHands = copy.deepcopy(hands)

        print "Connection opened with client."
        print "Wave to start hand tracking."

    # Websocket connection closed with client
    # Stop loop from running.
    def on_close(self):
        self.callback.stop()
        print "Connection closed with client."

    # Loop to handle input from OpenNI / Kinect
    # and send information to client
    def loop(self):

        global hands
        global tracking
        global q

        # Poll for updates from OpenNI / Kinect
        tracking.context.wait_any_update_all() 

        # If gesture is in the queue, send message to client.
        while not q.empty():
            self.write_message(q.get())

        # Send hand coordinates to client.
        if hands != self.lastHands:
            self.lastHands = copy.deepcopy(hands)
            self.send_xy()


    # Hand movement detected, so send message to client.
    def send_xy(self):

        global hands

        message = hands
        message["type"] = "hands"
        self.write_message(message)

    def on_message(self, message):
        pass
    

    # Allow cross origin requests
    def check_origin(self, origin):
        return True



application = tornado.web.Application([
    (r'/ws', WSHandler)
])
         
if __name__ == "__main__":
    print "Waiting for connection to client..."
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()



 