import subprocess
import thread
import time
from random import choice

import dropbox
import websocket

import settings
from index import Index
from keys import app_key, app_secret


access_token = ''
idx = None
light_on = False


def play_audio_mac():
    sound = "sounds/R2D2" + choice(["a", "b", "c", "e"]) + ".wav"
    return_code = subprocess.call(["afplay", sound])


def play_audio_ubuntu(letter):
    sound = "sounds/R2D2" + letter + ".wav"
    import pygame
    pygame.mixer.Sound(sound).play()


def on_message(ws, message):
    print message
    if access_token and "photo" in message:
        date_time = time.strftime("IMG_%Y-%m-%d_%H:%M:%S.png", time.gmtime())
        idx.take_picture(date_time)
        f = open(settings.base_path + 'pics/' + date_time)
        client = dropbox.client.DropboxClient(access_token)
        response = client.put_file('/' + date_time, f)
        print "Uploaded: ", response
    elif "pen" in message:
        print "Finding pen"
        idx.point_at_obj("pen")
        play_audio_ubuntu("c")
    elif "arduino" in message:
        print "Finding Arduino"
        idx.point_at_obj("arduino")
        play_audio_ubuntu("c")
    elif "keys" in message:
        print "Finding keys"
        idx.point_at_obj("key")
        play_audio_ubuntu("c")
    elif "spot" in message:
        print "Beep beep"
        play_audio_ubuntu("a")
    elif "lights" in message:
        global light_on
        light_on = not light_on
        print "Flipping light to " + str(light_on)
        idx.lazr.lamp(int(light_on))
        play_audio_ubuntu("a")
    #play_audio_mac()


def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"

def on_open(ws):
    global idx
    idx = Index()
    def run():
        while idx.step():
            pass
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    f = open('db_accesstoken.txt', 'r')
    access_token = f.readline()
    if not access_token:
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        authorize_url = flow.start()
        print authorize_url
        code = raw_input("Enter the authorization code here: ").strip()
        access_token, user_id = flow.finish(code)
        f = open('db_accesstoken.txt', 'w')
        f.write(access_token)
        f.close()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://pythonscript.richiezeng.com:8888/ws",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
