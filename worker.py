from socket import *
import os
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config


def calc_CC(filename, cc_config):
	file = open(filename, 'r')

	results = CCHarvester(filename, cc_config).gobble(file)

	file_cc = 0

	for i in results:
		print (i.complexity)
		file_cc += int(i.complexity)

	avg_cc = file_cc/ len(results)
	print("Total complexity of file: " + str(file_cc))
	print("Average complexity of file: " + str(avg_cc))
	return avg_cc

def main():
	
	cc_config = Config(
		exclude='',
		ignore='venv',
		order=SCORE,
		no_assert=True,
		show_closures=False,
		min='A',
		max='F',
	)

	CC_socket = socket(AF_INET, SOCK_STREAM)
	serverName = 'localhost'
	serverPort = 1234  
	CC_socket.bind(('', serverPort))
	CC_socket.listen(1)

	while True:
		connectionSocket, addr = CC_socket.accept()
		path = connectionSocket.recv(1024)
		path = path.decode()

		avg_cc = calc_CC(path, cc_config)
		avg_cc = str(avg_cc)
		connectionSocket.send(avg_cc.encode())

	connectionSocket.close()


if __name__ == "__main__":
	main()

