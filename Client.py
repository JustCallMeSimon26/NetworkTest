#This is the Client Side of the chat program.
#This program will send a message to the server.
import time

def test_message():
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()
	port = 9999
	s.connect((host, port))
	message = s.recv(1024)
	print(message.decode('ascii'))
	time.sleep(10)

if __name__ == '__main__':
	test_message()