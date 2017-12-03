from socket import *
import requests
from collections import deque
import shutil

def get_sha_list(github_url):
	sha_list = []

	token = get_token()
	payload = {'access_token': token}
	headers = {'Accept': 'application/vnd.github.v3.raw'}
	resp = requests.get(github_url,   params=payload, headers=headers)

	for item in resp.json():
		sha_list.append(item['sha'])

	return sha_list

def get_raw_url_list(github_url, sha_list):

	raw_url_list = []
	token = get_token()
	payload = {'access_token': token}
	headers = {'Accept': 'application/vnd.github.v3.raw'}
	for sha in sha_list:
		resp = requests.get(github_url + '/' + sha,  params=payload, headers=headers)
		#print(resp.json()['files'])
		files = {}
		files = resp.json()['files']
		print(files)
		print()
		if len(files) != 0:
			file_dict = files[0]
			raw_url_list.append(file_dict['raw_url'])
	return raw_url_list

	#print(raw_url)
	
	#resp = requests.get(raw_url)
	#print(resp.text)
	#with open('filetest.txt', 'w') as tmp_file:
	#			tmp_file.write(resp.text)

def get_token():
	with open('github-token.txt', 'r') as tmp_file:
		token = tmp_file.read()

	#token = 'access_token '+token
	print(token)
	return token

def main():

	github_url = 'https://api.github.com/repos/JTODR/Chat-Server-Project/commits'

	sha_list = get_sha_list(github_url)
	raw_url_list = get_raw_url_list(github_url, sha_list)
	print (raw_url_list)
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