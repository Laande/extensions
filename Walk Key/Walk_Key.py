# --------------------

WALK_OUT = 'MoveAvatar' # 0000 work too (replace 0000 with your header)

# --------------------

import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction
from g_python.hpacket import HPacket
from pynput import keyboard
from pynput.keyboard import Key, Controller

extension_info = {
    "title": "Walk with keyboard",
    "description": "Use numeric keypad",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()

x, y = None, None
k = Controller()


def on_press(key):
    global x, y
    
    if ext.is_closed():
        return False

    if x and y:
        try:
            if key == Key.home or key.vk == 103:
                x -= 1
                y += 1
                out()

            if key == Key.up or key.vk == 104:
                x -= 1
                out()

            if key == Key.page_up or key.vk == 105:
                x -= 1
                y -= 1
                out()

            if key == Key.left or key.vk == 100:
                y += 1
                out()

            if key == Key.right or key.vk == 102:
                y -= 1
                out()

            if key == Key.end or key.vk == 97:
                x += 1
                y += 1
                out()

            if key == Key.down or key.vk == 98:
                x += 1
                out()

            if key == Key.page_down or key.vk == 99:
                x += 1
                y -= 1
                out()
        except AttributeError:
            pass


def out():
    k.press(Key.backspace)
    ext.send_to_server(HPacket(WALK_OUT, x, y))


def coord(p):
    global x, y
    x, y = p.packet.read('ii')


ext.intercept(Direction.TO_SERVER, coord, WALK_OUT)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
