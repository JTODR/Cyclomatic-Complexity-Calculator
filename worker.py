from socket import *
import os
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
import requests
from time import gmtime, strftime
import os.path
import sys
import shutil


cc_config = Config(
		exclude='',
		ignore='venv',
		order=SCORE,
		no_assert=True,
		show_closures=False,
		min='A',
		max='F',
)


def get_filename(raw_url):

	sha_filename = raw_url.split('raw')[1]
	filename = sha_filename.split('/')[2]
	return filename

def calc_CC(raw_url, cc_config):

	filename = get_filename(raw_url)
	if filename.split('.')[1] != 'py':
		return -1


	resp = requests.get(raw_url)

	filename = strftime("%Y%m%d%H%M%S", gmtime()) + '.py'

	file_path = filename    
	with open(file_path, 'w') as tmp_file:
		tmp_file.write(resp.text)
	tmp_file.close()

	CC_file_get = open(file_path, 'r')
	results = CCHarvester(file_path, cc_config).gobble(CC_file_get)
	CC_file_get.close()
	os.remove(file_path)

	file_cc = 0

	for i in results:
		print (i.complexity)
		file_cc += int(i.complexity)

	#avg_cc = file_cc/ len(results)
	print("Complexity of file: " + str(file_cc))
	#print("Average complexity of file: " + str(avg_cc))
	return file_cc

def receive_work():

	CC_socket = socket(AF_INET, SOCK_STREAM)
	serverName = 'localhost'
	serverPort = 1598  
	CC_socket.bind(('', serverPort))
	CC_socket.listen(1)

	while True:
		connectionSocket, addr = CC_socket.accept()
		raw_url = connectionSocket.recv(1024)
		raw_url = raw_url.decode()

		print("RECEIVED: " + raw_url)

		file_cc = calc_CC(raw_url, cc_config)
		
		file_cc = str(file_cc)
		connectionSocket.send(file_cc.encode())

	connectionSocket.close()


def main():

	print("Worker is ready to receive...")
	receive_work()

if __name__ == "__main__":
	main()