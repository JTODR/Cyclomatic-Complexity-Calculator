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
		#print(files)
		#print(sha)
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
	#print(token)
	return token

def main():

	github_url = 'https://api.github.com/repos/JTODR/Distributed-File-System-Project/commits'

	print("Getting SHA list...")
	sha_list = get_sha_list(github_url)
	print("SHA list received...")
	print("Gettng raw URL's...")
	raw_url_list = get_raw_url_list(github_url, sha_list)
	print (raw_url_list)
	#raw_url_list = ['https://github.com/JTODR/Chat-Server-Project/raw/157f5205798d9e1d49dff5599dfba8cb092c9191/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/b8f732770a66597395438174efb932043c3e3110/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/0c20712232ce0a1c7a5937ea52b4482d00ff4f74/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/0d32735cbcaeb11651eec31decae6ec789bdfb1f/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/237bd1cc73bea0642556531c3d342e440712e46b/chat_server_util.py', 'https://github.com/JTODR/Chat-Server-Project/raw/c413bc26d5995b0bd28e3cbaa714411e852f31a2/chat_server_util.py', 'https://github.com/JTODR/Chat-Server-Project/raw/938ef5f469156a62c90fe027e4d9521a404372bf/chat_server.py', 'https://github.com/JTODR/Chat-Server-Project/raw/60fca4c621f6a58933824809b66ed16ab2c421d1/chat_server_util.py', 'https://github.com/JTODR/Chat-Server-Project/raw/1016b974e5b09572d76518abcafb9ab827249d19/chat_server.py', 'https://github.com/JTODR/Chat-Server-Project/raw/4c1720c0d2a773b906b18dcc9a634b8b3051c8f1/chat_server.py', 'https://github.com/JTODR/Chat-Server-Project/raw/1e517ff06331596b04ab7c30dcd7a21828d4df12/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/99504dfa50bcce3b1c015142f06b043390aacba5/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/92c0944cfb71210f0fa99ae4b1f3c66f645c97c3/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/99504dfa50bcce3b1c015142f06b043390aacba5/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/604d57833b6313f7737a3df9b9319978081d9b34/chat_server_util.py', 'https://github.com/JTODR/Chat-Server-Project/raw/92c0944cfb71210f0fa99ae4b1f3c66f645c97c3/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/b505ea5949ce560701ca477e04673501e0bfd01b/README.md', 'https://github.com/JTODR/Chat-Server-Project/raw/cffbdd25c67b54ff0d8c12e100232b92ae0efac6/chat_server.py']
	serverName = 'localhost'
	serverPort = 1598  
	
	#path_list = ['C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\client_lib.py',
	#'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\client.py',
	#'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\locking_service.py',
	#'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\file_server.py',
	#'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\directory_service.py']


	print("Commenced sending of raw URL's to worker...")
	total_cc = 0

	for path in raw_url_list:
		manager_socket = socket(AF_INET, SOCK_STREAM)
		manager_socket.connect((serverName,serverPort))
		manager_socket.send(path.encode())
		print("SENT: " + path)
		reply = manager_socket.recv(1024)
		reply = reply.decode()
		print("RECEIVED: " + reply)
		if reply != "-1" and reply is not None:
			#print(reply.decode())
			reply = int(reply)
			total_cc += reply 
		manager_socket.close()

	print("Total CC is: " + str(total_cc))
	avg_cc = total_cc/len(raw_url_list)
	print("Average CC is: " + str(avg_cc))

if __name__ == "__main__":
	main()