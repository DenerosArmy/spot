import tornado.ioloop
import tornado.web

connection = None


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class SpeechHandler(tornado.web.RequestHandler):
    def get(self):
        word = self.get_argument('word', True)
        print word
        #connection.write_message(word)


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        connection = self
        self.write_message("Hi, client: connection is made ...")

    def on_message(self, message):
        print 'message received: \"%s\"' % message

    def on_close(self):
        print 'connection closed'

    def test(self):
        self.write_message("scheduled!")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r'/ws', WSHandler),
    (r'/speech', SpeechHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
