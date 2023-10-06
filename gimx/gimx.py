import socket
from enum import IntEnum
from time import sleep
import struct
import sys

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 51914


class Ps4Controls(IntEnum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    RIGHT_STICK_X = 2
    RIGHT_STICK_Y = 3
    FINGER1_X = 4
    FINGER1_Y = 5
    FINGER2_X = 6
    FINGER2_Y = 7
    SHARE = 128
    OPTIONS = 129
    PS = 130
    UP = 131
    RIGHT = 132
    DOWN = 133
    LEFT = 134
    TRIANGLE = 135
    CIRCLE = 136
    CROSS = 137
    SQUARE = 138
    L1 = 139
    R1 = 140
    L2 = 141
    R2 = 142
    L3 = 143
    R3 = 144
    TOUCHPAD = 145
    FINGER1 = 146
    FINGER2 = 147

class XboxOneControls(IntEnum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    RIGHT_STICK_X = 2
    RIGHT_STICK_Y = 3
    VIEW = 128
    MENU = 129
    GUIDE = 130
    UP = 131
    RIGHT = 132
    DOWN = 133
    LEFT = 134
    Y = 135
    B = 136
    A = 137
    X = 138
    LB = 139
    RB = 140
    LT = 141
    RT = 142
    LS = 143
    RS = 144


class ButtonState(IntEnum):
    RELEASED = 0
    PRESSED = 255


def send_message(ip, port, changes):
    
    packet = bytearray([0x01, len(changes)])  # type + axis count
    
    for axis, value in changes.items():
        # axis + value (network byte order)
        packet.extend([axis, (value & 0xff000000) >> 24, (value & 0xff0000) >> 16, (value & 0xff00) >> 8, (value & 0xff)])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (ip, port))


def check_status(ip, port):
    
    packet = bytearray([0x00, 0x00])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((ip, port))
    sock.send(packet)
    timeval = struct.pack('ll', 1, 0)  # seconds and microseconds
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
    try:
        data, (address, port) = sock.recvfrom(2)
        response = bytearray(data)
        if (response[0] != 0x00):
            print("Invalid reply code: {0}".format(response[0]))
            return 1
    except socket.error as err:
        print(err)
    
    return 0


def main():
    
    ip = DEFAULT_IP
    port = DEFAULT_PORT
    
    if check_status(ip, port):
        sys.exit(-1)

    changes = { Ps4Controls.PS: ButtonState.PRESSED }
    send_message(ip, port, changes)
    sleep(0.05)
    changes[Ps4Controls.PS] = ButtonState.RELEASED
    send_message(ip, port, changes)   
    sleep(0.05)

    send_message(ip, port, { Ps4Controls.PS: ButtonState.PRESSED })
    sleep(0.05)
    send_message(ip, port, { Ps4Controls.PS: ButtonState.RELEASED })   
    sleep(0.05)
     
    for value in [-32767, -127, -1, 0, 1, 127, 32767]:
        send_message(ip, port, { Ps4Controls.LEFT_STICK_X: value })
        sleep(0.05)
    
    send_message(ip, port, { Ps4Controls.LEFT_STICK_X: 0 })
    sleep(0.05)
    
    send_message(ip, port, { Ps4Controls.LEFT_STICK_X: 127, Ps4Controls.LEFT_STICK_Y: 127 })
    sleep(0.05)
    
    send_message(ip, port, { Ps4Controls.LEFT_STICK_X: 0, Ps4Controls.LEFT_STICK_Y: 0 })
    sleep(0.05)
    
    state = {
        Ps4Controls.LEFT_STICK_X : 127,
        Ps4Controls.LEFT_STICK_Y : 0,
        Ps4Controls.RIGHT_STICK_X : 0,
        Ps4Controls.RIGHT_STICK_Y : 0,
        Ps4Controls.FINGER1_X : 0,
        Ps4Controls.FINGER1_Y : 0,
        Ps4Controls.FINGER2_X : 0,
        Ps4Controls.FINGER2_Y : 0,
        Ps4Controls.SHARE : ButtonState.RELEASED,
        Ps4Controls.OPTIONS : ButtonState.RELEASED,
        Ps4Controls.PS : ButtonState.RELEASED,
        Ps4Controls.UP : ButtonState.RELEASED,
        Ps4Controls.RIGHT : ButtonState.RELEASED,
        Ps4Controls.DOWN : ButtonState.RELEASED,
        Ps4Controls.LEFT : ButtonState.RELEASED,
        Ps4Controls.TRIANGLE : ButtonState.RELEASED,
        Ps4Controls.CIRCLE : ButtonState.RELEASED,
        Ps4Controls.CROSS : ButtonState.RELEASED,
        Ps4Controls.SQUARE : ButtonState.RELEASED,
        Ps4Controls.L1 : ButtonState.RELEASED,
        Ps4Controls.R1 : ButtonState.RELEASED,
        Ps4Controls.L2 : ButtonState.RELEASED,
        Ps4Controls.R2 : ButtonState.RELEASED,
        Ps4Controls.L3 : ButtonState.RELEASED,
        Ps4Controls.R3 : ButtonState.RELEASED,
        Ps4Controls.TOUCHPAD : ButtonState.RELEASED,
        Ps4Controls.FINGER1 : ButtonState.RELEASED,
        Ps4Controls.FINGER2 : ButtonState.RELEASED,
        }
    # all controls released except left stick x
    send_message(ip, port, state)
    sleep(0.05)
    
    state[Ps4Controls.LEFT_STICK_X] = 0
    # all controls released
    send_message(ip, port, state)
    sleep(0.05)
    
    full_state = {
        Ps4Controls.LEFT_STICK_X : 127,
        Ps4Controls.LEFT_STICK_Y : 127,
        Ps4Controls.RIGHT_STICK_X : 127,
        Ps4Controls.RIGHT_STICK_Y : 127,
        Ps4Controls.FINGER1_X : 919,
        Ps4Controls.FINGER1_Y : 1919,
        Ps4Controls.FINGER2_X : 919,
        Ps4Controls.FINGER2_Y : 1919,
        Ps4Controls.SHARE : ButtonState.PRESSED,
        Ps4Controls.OPTIONS : ButtonState.PRESSED,
        Ps4Controls.PS : ButtonState.PRESSED,
        Ps4Controls.UP : ButtonState.PRESSED,
        Ps4Controls.RIGHT : ButtonState.PRESSED,
        Ps4Controls.DOWN : ButtonState.PRESSED,
        Ps4Controls.LEFT : ButtonState.PRESSED,
        Ps4Controls.TRIANGLE : ButtonState.PRESSED,
        Ps4Controls.CIRCLE : ButtonState.PRESSED,
        Ps4Controls.CROSS : ButtonState.PRESSED,
        Ps4Controls.SQUARE : ButtonState.PRESSED,
        Ps4Controls.L1 : ButtonState.PRESSED,
        Ps4Controls.R1 : ButtonState.PRESSED,
        Ps4Controls.L2 : ButtonState.PRESSED,
        Ps4Controls.R2 : ButtonState.PRESSED,
        Ps4Controls.L3 : ButtonState.PRESSED,
        Ps4Controls.R3 : ButtonState.PRESSED,
        Ps4Controls.TOUCHPAD : ButtonState.PRESSED,
        Ps4Controls.FINGER1 : ButtonState.PRESSED,
        Ps4Controls.FINGER2 : ButtonState.PRESSED,
        }
    # all controls activated
    send_message(ip, port, full_state)
    sleep(0.05)
    
    empty_state = {
        Ps4Controls.LEFT_STICK_X : 0,
        Ps4Controls.LEFT_STICK_Y : 0,
        Ps4Controls.RIGHT_STICK_X : 0,
        Ps4Controls.RIGHT_STICK_Y : 0,
        Ps4Controls.FINGER1_X : 0,
        Ps4Controls.FINGER1_Y : 0,
        Ps4Controls.FINGER2_X : 0,
        Ps4Controls.FINGER2_Y : 0,
        Ps4Controls.SHARE : ButtonState.RELEASED,
        Ps4Controls.OPTIONS : ButtonState.RELEASED,
        Ps4Controls.PS : ButtonState.RELEASED,
        Ps4Controls.UP : ButtonState.RELEASED,
        Ps4Controls.RIGHT : ButtonState.RELEASED,
        Ps4Controls.DOWN : ButtonState.RELEASED,
        Ps4Controls.LEFT : ButtonState.RELEASED,
        Ps4Controls.TRIANGLE : ButtonState.RELEASED,
        Ps4Controls.CIRCLE : ButtonState.RELEASED,
        Ps4Controls.CROSS : ButtonState.RELEASED,
        Ps4Controls.SQUARE : ButtonState.RELEASED,
        Ps4Controls.L1 : ButtonState.RELEASED,
        Ps4Controls.R1 : ButtonState.RELEASED,
        Ps4Controls.L2 : ButtonState.RELEASED,
        Ps4Controls.R2 : ButtonState.RELEASED,
        Ps4Controls.L3 : ButtonState.RELEASED,
        Ps4Controls.R3 : ButtonState.RELEASED,
        Ps4Controls.TOUCHPAD : ButtonState.RELEASED,
        Ps4Controls.FINGER1 : ButtonState.RELEASED,
        Ps4Controls.FINGER2 : ButtonState.RELEASED,
        }
    # all controls released
    send_message(ip, port, empty_state)
    sleep(0.05)


if __name__ == "__main__":
    main()