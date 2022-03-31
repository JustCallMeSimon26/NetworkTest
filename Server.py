import socket 
import threading
import requests
import time
import numpy as np
from PIL import Image
import random
from os import system

class Logic:
	def __init__(self):
		self.inactivePixels = []
		self.activePixels = []
		self.startX = None
		self.startY = None
		self.loadImage()
		self.updateTitleThread = threading.Thread(target=self.updateTitle)
		self.updateTitleThread.start()
	
	def loadImage(self):
		self.image = Image.open("download.jpg")
		self.pixels = self.image.load()
		self.width, self.height = self.image.size
		self.imageArray = np.array(self.image)
		for x in range(self.width):
			for y in range(self.height):
				self.inactivePixels.append((x,y))

	def switchPixelState(self, pixel):
		if pixel in self.inactivePixels:
			self.inactivePixels.remove(pixel)
			self.activePixels.append(pixel)
		elif pixel in self.activePixels:
			self.activePixels.remove(pixel)
			self.inactivePixels.append(pixel)

	def getFreePixel(self, onetime=False):
		Pixel = random.choice(self.inactivePixels) 
		if not onetime:
			self.switchPixelState(Pixel)
		return Pixel

	def updateTitle(self):
		while True:
			system(f"title Users:{threading.activeCount() - 1} ^| Pixels:{len(self.activePixels)}/{len(self.inactivePixels)+len(self.activePixels)}")

class Server:
	def __init__(self):
		self.HEADER = 64
		self.SERVER = socket.gethostbyname(socket.gethostname()) #ip goes here
		self.PORT = 5050 #port goes here
		self.ADDR = (self.SERVER, self.PORT) #full server adress
		self.setup()

	def setup(self):
		self.Logic = Logic()

	def start(self):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(self.ADDR)
		server.listen()
		print(stampIt(f"Started server on {self.SERVER}:{self.PORT}"))
		while True:
			conn, addr = server.accept()
			thread = threading.Thread(target=self.handle_client, args=(conn, addr))
			thread.start()

	def handle_client(self, conn, addr):
		locData = requests.get(f"https://geolocation-db.com/json/{conn}&position=true").json()    
		print(stampIt(f"New Anonymous User from {locData['country_name']} connected."))
		Pixel = self.Logic.getFreePixel() #dont know what this returns
		connected = True
		self.sendMessage(conn, f"#dont know what goes here exactly")
		while connected:
			msg_length = conn.recv(self.HEADER).decode("utf-8")
			if msg_length:
				msg_length = int(msg_length)
				msg = conn.recv(msg_length).decode("utf-8")
				#Handle Client disconnecting
				print(stampIt(msg))
				if msg == "disconnect":
					connected = False
				elif msg == "otp":
					Pixel = self.Logic.getFreePixel(onetime=True)			
					self.sendMessage(conn, f"#dont know what goes here exactly")
				#implement following messages:
				#-want pixel
				#-has send pixel
				#how to send back:
				#conn.send("Disconnecting".encode("utf-8"))	
		conn.close()
		Logic.switchPixelState(Pixel)
		print(stampIt(f"Anonymous User from {location} disconnected."))

	def sendMessage(self, conn, msg):
		message = msg.encode("utf-8")
		msg_length = len(message)
		send_length = str(msg_length).encode("utf-8")
		send_length += b' ' * (self.HEADER - len(send_length))
		conn.send(send_length)
		conn.send(message)

#Helper Methods
def stampIt(message):
	timestamp = timestamp = time.strftime("%H:%M:%S")
	return f"@{timestamp} [HYDRA] {message}"


if __name__ == '__main__':
	urMom = Server()
	urMom.setup()
	urMom.start()