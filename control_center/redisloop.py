from .tello import Tello
from .utils import get_wifi
import cv2
import redis
import threading
import time

class RedisHander:
    running = False
    throttle = 0.07
    client = redis.Redis(host="45.77.214.239", port = 6379)
    subscribe = client.pubsub()
    video_thread = None
    command_thread = None
    pubhlish_thread = None
    FRAME = None

    def _video(self):
        video_capture = cv2.VideoCapture("udp://0.0.0.0:11111")
        n = 0
        while self.running:
            return_key, frame = video_capture.read()
            if frame is None:
                continue
            n += 1
            scale_percent = 40 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

            return_key, encoded_image = cv2.imencode(".jpg", resized)
            if n % 50 == 0:
                print("frames alive")
            self.FRAME = b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n'
    
    def _publish(self):
        while self.running:
            time.sleep(self.throttle)
            print("sending frame")
            if self.FRAME:
                self.client.publish("dev", self.FRAME)

    def publish(self):
        self.pubhlish_thread = threading.Thread(target=self._publish)
        self.pubhlish_thread.start()
    
    def _command(self):
        self.subscribe.subscribe("commands")
        while self.running:
            message = self.subscribe.get_message()
            if message and message["data"] != 1:
                command = message["data"]
                print(command)
                Tello.command(command)

    def video(self):
        self.video_thread = threading.Thread(target=self._video)
        self.video_thread.start()

    def command_loop(self):
        self.command_thread = threading.Thread(target=self._command)
        self.command_thread.start()

    def checker(self):
        while self.running:
            time.sleep(15)
            print("-- Checking Wifi --")
            if "TELLO" not in get_wifi():
                self.running = False
                self.run()





    def run(self):
        Tello.connect()
        Tello.command(b"streamon")
        print("streaming")
        self.running = True
        self.video()
        self.command_loop()
        self.publish()
        self.checker()