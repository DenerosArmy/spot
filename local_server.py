import thread
import time

import dropbox
import websocket

from keys import app_key, app_secret


access_token = ''


def on_message(ws, message):
    print message
    if 'picture' in message and access_token:
        date_time = time.strftime("IMG_%Y-%m-%d_%H:%M:%S.png", time.gmtime())
        client = dropbox.client.DropboxClient(access_token)
        f = open('working-draft.txt', 'w+')
        response = client.put_file('/' + date_time, f)
        print "Uploaded: ", response


def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"


if __name__ == "__main__":
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    print authorize_url
    code = raw_input("Enter the authorization code here: ").strip()
    access_token, user_id = flow.finish(code)

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://pythonscript.richiezeng.com:8888/ws",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.run_forever()
