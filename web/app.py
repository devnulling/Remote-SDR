from tornado import websocket, escape, web, ioloop, gen
import json
import datetime
import os

cl = []

class SocketHandler(websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True
	def open(self):
		if self not in cl:
			cl.append(self)
	def on_close(self):
		if self in cl:
			cl.remove(self)
	def on_message(self, message):
		for c in cl:
			c.write_message(message)

class InputHandler(web.RequestHandler):
	def post(self, *args):
		data = web.escape.json_decode(self.request.body)

		self.finish()

		for c in cl:
			c.write_message(data)

class HomeHandler(web.RequestHandler):
    def get(self):
        self.render('static/templates/remote_sdr.html')


path = os.path.join(os.getcwd(), 'static')
settings = {
	'debug':True,
}

if __name__ == "__main__":
    application = web.Application(
        [
            (r'/', HomeHandler),
            (r'/ws', SocketHandler),
            (r'/input', InputHandler),
            (r'/static/(.*\..*)', web.StaticFileHandler, {'path': path})
        ],
        **settings)


    application.listen(8000)
    ioloop.IOLoop.current().start()
