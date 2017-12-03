from socket import *


def main():
	serverName = 'localhost'
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
		manager_socket.close()


if __name__ == "__main__":
	main()