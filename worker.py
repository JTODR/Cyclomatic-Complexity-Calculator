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

from re import match

cc_config = Config(
        exclude='',
        ignore='venv',
        order=SCORE,
        no_assert=True,
        show_closures=False,
        min='A',
        max='F',
)

def get__params_headers():
    with open('github-token.txt', 'r') as tmp_file:
        token = tmp_file.read()     # get the token from a text file in current directory

    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}

    #print(token)
    return (payload, headers)


def check_py(filename):
    return True if match('.*\.py', filename) is not None else False

def calc_CC(raw_url, cc_config):

    blob_url = raw_url.split('|')[0]
    filename = raw_url.split('|')[1]

    payload_headers = get__params_headers()

    flag = check_py(filename)
    if flag == True:

        resp = requests.get(blob_url,   params=payload_headers[0], headers=payload_headers[1])

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
    else:
        return -1

def receive_work():
    serverName = 'localhost'
    serverPort = 2017 

    CC_socket = socket(AF_INET, SOCK_STREAM)
    CC_socket.connect((serverName,serverPort))

    msg = "Ready|Worker1"

    CC_socket.send(msg.encode())

    '''
    CC_socket = socket(AF_INET, SOCK_STREAM)
    serverName = 'localhost'
    serverPort = 1598  
    CC_socket.bind(('', serverPort))
    CC_socket.listen(1)
    '''

    while True:
        #connectionSocket, addr = CC_socket.accept()
        raw_url = CC_socket.recv(1024)
        raw_url = raw_url.decode()

        print("RECEIVED: " + raw_url)

        file_cc = calc_CC(raw_url, cc_config)
        
        file_cc = str(file_cc)
        CC_socket.send(file_cc.encode())

    CC_socket.close()


def main():

    print("Worker is ready to receive...")
    receive_work()

if __name__ == "__main__":
    main()