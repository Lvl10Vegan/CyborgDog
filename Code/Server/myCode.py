#Import everything in the control module, 
#including functions, classes, variables, and more.

from Control import *
from Buzzer import *
import random
import pickle
from socket import *
import sys

#Creating object 'control' of 'Control' class.
control=Control()

buzzer = Buzzer()

def randMotion():
	rand = random.randInt(1,4)
	
	if rand == 1:
		#Using the forWard function, let the robot dog move forward five steps and keep standing.
		for i in range(5):
			control.forWard()
		control.stop()

	if rand == 2:
		#Turn the robot dog's body 10 degrees to the right
		for i in range(10):
			control.attitude(0,0,i)
			time.sleep(0.1)

	if rand == 3:
		#Turn the robot dog's body 20 degrees to the left	
		for i in range(10,-10,-1):
			control.attitude(0,0,i)
			time.sleep(0.1)

	else:	
		#Straighten the robot dog's body
		for i in range(-10,0,1):
			control.attitude(0,0,i)
			time.sleep(0.1)	



# Main program logic follows:
if __name__ == '__main__':
	print ('Program is starting ... ')
	if len(sys.argv)<2:
        print ("Parameter error: Please enter host IP address")
        exit()

	else:
		host_ip = sys.argv[1]
		# Socket Create
		socket = socket(AF_INET, SOCK_STREAM)

		#host_ip = gethostbyname(gethostname())
		# empty host_ip accepts all connections (wildcard)
		print('HOST IP:', host_ip) 
		port = 5050 # make sure port number matches the one in Send.py
		socket_address = (host_ip, port)

		socket.bind(socket_address)
		socket.listen(5)
		client_socket, addr = socket.accept()

		if client_socket:
			while True:
				pickMsg = client_socket.recv(64)
				msg = int(pickle.loads(pickMsg))
				if msg == 1:
					buzzer.run(1)
					time.sleep(0.5)
					buzzer.run(0)	
					randMotion()
		
