import socket
class Client:
	def __init__(self):
		self.HEADER = 64
		self.PORT = 5050
		self.SERVER = socket.gethostbyname(socket.gethostname())
		self.ADDR = (self.SERVER, self.PORT)
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect()
		self.listen()
		self.placedThisSession = 0

	def connect(self):
		self.client.connect(self.ADDR)
		self.connected = True

	def listen(self):
		while self.connected:
			msg_length = client.recv(self.HEADER).decode("utf-8")
			if msg_length:
				msg_length = int(msg_length)
				msg = client.recv(msg_length).decode("utf-8")
				self.useMessage(msg)

	def useMessage(self, msg):
		try:
			x,y,color = msg
			self.placePixel(x,y,color)
		except:
			pass
		#parse message

	def placePixel(self, x, y, color):
		status = self.checkPixel()
		if status == "repair":
			pass #placing here
			self.placedThisSession += 1
		elif status == "good":
			self.requestOneTimePixel()
		#smth smth update stats tracker for user
		#cant even theorise about this yet lol

	def sendMessage(self, msg):
		message = msg.encode("utf-8")
		msg_length = len(message)
		send_length = str(msg_length).encode("utf-8")
		send_length += b' ' * (HEADER - len(send_length))
		client.send(send_length)
		client.send(message)

if __name__ == '__main__':
	UrDad = Client()