from os import stat
import socket
import time
from .utils import get_wifi

class Tello:
    SINGLE_TELLO_IP = "192.168.10.1"
    COMMAND_PORT: int = 8889
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    running = False

    @classmethod
    def connect(cls):
        wifi = get_wifi()
        if "TELLO" in wifi:
            print("Wifi Connect")
            try:
                cls.SOCKET.connect((cls.SINGLE_TELLO_IP, cls.COMMAND_PORT))
                cls.SOCKET.send(b"command")
                print("Command sent")
            except:
                print("trying to connect again.")
                time.sleep(5)
                cls.connect()
        else:
            print(wifi)
            time.sleep(5)
            cls.connect()
    
    @classmethod
    def command(cls, command):
        cls.SOCKET.send(command)