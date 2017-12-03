from socket import *
import requests
from collections import deque
import shutil

def get_github_file():
	commits_list = []

	resp = requests.get(
		'https://api.github.com/repos/JTODR/Chat-Server-Project/commits')

	for item in resp.json():
		commits_list.append(item['sha'])
		#print(item)

	#print(len(commits_list))
	#print(commits_list)
	#print(commits_list[0])


	resp = requests.get(
		'https://api.github.com/repos/JTODR/Chat-Server-Project/commits/' + commits_list[0])
	print(resp.json()['files'])
	files = {}
	files = resp.json()['files']
	file_dict = files[0]

	blob_url = file_dict['raw_url']
	print(blob_url)
	
	resp = requests.get(blob_url)
	with open('filetest.txt', 'w') as tmp_file:
				tmp_file.write(resp.text)


def main():
	
	get_github_file()
	'''serverName = 'localhost'
	serverPort = 1234  
	
	path_list = ['C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\client_lib.py',
	'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\client.py',
	'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\locking_service.py',
	'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\file_server.py',
	'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\directory_service.py']

	for path in path_list:
		manager_socket = socket(AF_INET, SOCK_STREAM)
		manager_socket.connect((serverName,serverPort))
		manager_socket.send(path.encode())
		print("SENT: " + path)
		reply = manager_socket.recv(1024)
		print(reply.decode())
		manager_socket.close()'''


if __name__ == "__main__":
	main()