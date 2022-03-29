#This is the server side of the chat program.
#This program will listen for connections from the client and then
#send the message to all clients connected to the server.

def main():
	#Import the socket library
	import socket
	#Create a socket object
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#Get the local machine name
	host = socket.gethostname()
	port = 9999
	#Bind to the port
	s.bind((host, port))
	#Listens for connections
	s.listen(5)
	print('Server listening....')
	while True:
		#Accept connections
		c, addr = s.accept()
		print('Got connection from', addr)
		#Send a thank you message to the client.
		c.send('Thank you for connecting'.encode('ascii'))

if __name__ == '__main__':
	main()