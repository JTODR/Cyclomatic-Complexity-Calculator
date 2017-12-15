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
from time import gmtime, strftime
import time



class Worker():
    total_cc = 0
    manager_url = 'http://localhost:2020/'      # url of the flask server

    cc_config = Config(
            exclude='',
            ignore='venv',
            order=SCORE,
            no_assert=True,
            show_closures=False,
            min='A',
            max='F',
    )

    def __init__(self):
        self.blob_url = requests.get(self.manager_url).json()   # get the first url

    def get__params_headers(self):
        with open('github-token.txt', 'r') as tmp_file:
            token = tmp_file.read()     # get the token from a text file in current directory

        payload = {'access_token': token}
        headers = {'Accept': 'application/vnd.github.v3.raw'}

        #print(token)
        return (payload, headers)


    def check_py(self, filename):
        return True if match('.*\.py', filename) is not None else False

    def calc_CC(self, blob_url):

        url = blob_url.split('|')[0]
        filename = blob_url.split('|')[1]

        payload_headers = self.get__params_headers()

        flag = self.check_py(filename)
        if flag == True:

            resp = requests.get(url,   params=payload_headers[0], headers=payload_headers[1])

            curr_time = time.clock()
            curr_time = str(curr_time)
            curr_time = curr_time.split('.')[1]
            sha = url.split('/blobs/')[1]       # give the temp file a unique name (sha + current processor time)

            file_path = sha + curr_time  + '.py'

            with open(file_path, 'w') as tmp_file:
                tmp_file.write(resp.text)
            tmp_file.close()


            CC_file_get = open(file_path, 'r')
            results = CCHarvester(file_path, self.cc_config).gobble(CC_file_get)
            CC_file_get.close()
            os.remove(file_path)

            file_cc = 0

            for i in results:
                file_cc += int(i.complexity)

            print("Complexity of file: " + str(file_cc))

            return file_cc
        else:
            return 0

    def receive_work(self):

        file_cc = self.calc_CC(self.blob_url)
        self.total_cc += file_cc

        self.blob_url = requests.get(self.manager_url).json()
        while self.blob_url != "finished":
            file_cc = self.calc_CC(self.blob_url)
            self.total_cc += file_cc
            self.blob_url = requests.get(self.manager_url).json()


        print("Finished...") 
        print("Total CC: " + str(self.total_cc))
        requests.put(self.manager_url, data={'cc': self.total_cc})

def main():

    print("Worker is ready to receive...")
    worker = Worker()
    worker.receive_work()

if __name__ == "__main__":
    main()