from socket import *
import requests
from collections import deque
import shutil

def get_tree_urls(github_url):
	

	tree_urls = []

	payload_headers = get__params_headers()

	resp = requests.get(github_url,   params=payload_headers[0], headers=payload_headers[1])	# get the commit page of the github url

	for item in resp.json():
		tree_urls.append(item['commit']['tree']['url'])	# parse out the SHA's from the commit page

	return tree_urls


def get_blob_url_list(github_url, tree_urls):
	#count = 0
	blob_url_list = []
	payload_headers = get__params_headers()	
	for blob_url in tree_urls:
		resp = requests.get(blob_url,   params=payload_headers[0], headers=payload_headers[1])

		tree = resp.json()['tree']

		for item in tree:
			file_url = item['url']
			filename = item['path']

			url_filename = file_url + '|' + filename
			blob_url_list.append(url_filename)

	return blob_url_list

			#flag = check_py(filename)
			#if flag == True:

			#	resp = requests.get(file_url,   params=payload_headers[0], headers=payload_headers[1])

			#	filename = str(count)
			#	file_path = ".\\temp\\" + filename + '.py'  

			#	with open(file_path, 'w') as tmp_file:
			#		tmp_file.write(resp.text)
			#	tmp_file.close()
			#	count +=1
		#if count == 15:
			#break


'''
	raw_url_list = []

	payload_headers = get__params_headers()

	for tree in tree_urls:
		resp = requests.get(github_url + '/' + tree,  params=payload_headers[0], headers=payload_headers[1])		# get the individual commit from the current SHA
		files = {}
		files = resp.json()['files']	# parse out the files from that commit

		if len(files) != 0:
			file_dict = files[0]
			raw_url_list.append(file_dict['raw_url'])	# parse out the raw URL of the file 
	return raw_url_list
'''


def get__params_headers():
	with open('github-token.txt', 'r') as tmp_file:
		token = tmp_file.read()		# get the token from a text file in current directory

	payload = {'access_token': token}
	headers = {'Accept': 'application/vnd.github.v3.raw'}

	#print(token)
	return (payload, headers)

def send_work(raw_url_list):
	serverName = 'localhost'
	serverPort = 1598
	total_cc = 0

	count = 0

	# send URL's one by one to the worker
	for raw_url in raw_url_list:	
		manager_socket = socket(AF_INET, SOCK_STREAM)
		manager_socket.connect((serverName,serverPort))
		manager_socket.send(raw_url.encode())		
		print("SENT: " + raw_url)

		reply = manager_socket.recv(1024)	# receive the cyclomatic complexity for the file at the current raw URL
		reply = reply.decode()
		print("RECEIVED: " + reply)

		if reply != "-1" and reply is not None:
			reply = int(reply)
			total_cc += reply 		# increment total commit CC with the reply from the worker
			count += 1
		manager_socket.close()
	print ("Count = " + str(count))
	return total_cc

def main():

	#github_url = 'https://api.github.com/repos/JTODR/Distributed-File-System-Project/commits'
	github_url = 'https://api.github.com/repos/geekcomputers/Python/commits'

	print("Getting SHA list...")
	tree_urls = get_tree_urls(github_url)		# get the list of SHA's from the project's commits
	print("SHA list received...")
	print("Gettng raw URL's...")
	raw_url_list = get_blob_url_list(github_url, tree_urls)	# get raw URLs of the SHA's 
	print (raw_url_list)
	#raw_url_list = ['https://github.com/JTODR/Distributed-File-System-Project/raw/8386c342e144fd1e46ccea5e107112a36994a08e/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/7200a2e0c272f23f599f89afd5c801a64a80792e/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/af01ee7a4937fe332a040c371ad680c1eb849f73/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/f552ce7a2885abd76cd320641a5a8cfddd20fe00/client_lib.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/86dd0696922c6c8813a50b6953519bd57bf023dd/client_lib.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/ee6fdda9209ed1df254a00dcfb368fbcd28fedfd/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/0c803a0e386ad1fdcb02a7ada15b6231cfdf8b70/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/d4fa0dd716538033ba8ab05b8e0bdbe3080749e6/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/a4e3fc9278d44af8c5eef3a0c34cbbd9db64ad84/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/da7fc3d0316550b62fb05a6d8281a5dd74f1099d/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/f55911846ca73ea36c7ea16c0f307aaaf99552e2/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/5a3688855b908c70b625a2098085a8a7b8575f9f/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/9b5fa2b03a98a34b9e22665fd438b3f9435d8250/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/bb04b5d0569fcd05cf2527e0d0bd44011b2595cf/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/c8ad41520096c507eacad4ee419b85eb2094ad38/client.py', 'https://github.com/JTODR/Distributed-File-System-Project/raw/12b54f9da4fbe9e5077558eb9498a4406c171ae5/.gitignore', 'https://github.com/JTODR/Distributed-File-System-Project/raw/8c88429a266d63d7ad8db84c2722e1caf4c31ab2/.gitignore', 'https://github.com/JTODR/Distributed-File-System-Project/raw/c99def793705b300d4dbc7afeeb0c9de474fb63f/client.py']

	print("Commenced sending of raw URL's to worker...")
	#total_cc = send_work(raw_url_list)		# send the raw URL's to the worker

	#print("Total CC is: " + str(total_cc))	

	#avg_cc = total_cc/len(raw_url_list)
	#print("Average CC is: " + str(avg_cc))

if __name__ == "__main__":
	main()