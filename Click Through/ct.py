# --------------------

# Raw id (1234) work too
# just remove "Chat" with 1234 (for example)

SPEECH_OUT = "Chat"  # Packet (out) when you send a message
SPEECH_IN = "Chat"  # Packet (in) when somebody talk
IN_GAME = "YouArePlayingGame"  # Packet you receive when you join a team
ROOM_CHANGE = "RoomReady"  # Incoming enter in room

# --------------------

import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction
from g_python.hpacket import HPacket

extension_info = {
    "title": "Click Through",
    "description": "Let you click on user and walk in",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()


is_on = False


def speech(p):
    global is_on
    
    text, _, _ = p.packet.read('sii')

    if text.lower() == ":ct":
        p.is_blocked = True
        is_on = not is_on

        ext.send_to_client(HPacket(IN_GAME, (1 if is_on else 0)))
        ext.send_to_client(HPacket(SPEECH_IN, -1, "Click Through : " + ("Activated" if is_on else "Deactivate"), 0, 1, 0, 0))



def room_change(_):
    global is_on

    is_on = False


ext.intercept(Direction.TO_SERVER, speech, SPEECH_OUT)
ext.intercept(Direction.TO_CLIENT, room_change, ROOM_CHANGE)
