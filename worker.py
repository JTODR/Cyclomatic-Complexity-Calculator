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



class Worker():
    total_cc = 0
    manager_url = 'http://localhost:2020/'

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
        self.blob_url = requests.get(self.master_url).json()
        print(self.blob_url)

    def get__params_headers(self):
        with open('github-token.txt', 'r') as tmp_file:
            token = tmp_file.read()     # get the token from a text file in current directory

        payload = {'access_token': token}
        headers = {'Accept': 'application/vnd.github.v3.raw'}

        #print(token)
        return (payload, headers)


    def check_py(self, filename):
        return True if match('.*\.py', filename) is not None else False

    def calc_CC(self, raw_url):

        blob_url = raw_url.split('|')[0]
        filename = raw_url.split('|')[1]

        payload_headers = self.get__params_headers()

        flag = self.check_py(filename)
        if flag == True:

            resp = requests.get(blob_url,   params=payload_headers[0], headers=payload_headers[1])

            file_path = filename

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
            #print("Average complexity of file: " + str(avg_cc))
            return file_cc
        else:
            return 0

    def receive_work(self):

        print("Blob is: " + self.blob_url)

        file_cc = self.calc_CC(self.blob_url)
        self.total_cc += file_cc
        #print(str(file_cc))

        self.blob_url = requests.get(self.master_url).json()
        if self.blob_url != "finished":
            self.receive_work()
        else:
            print("Finished...") 
            print("Total CC: " + str(self.total_cc))
            requests.put(self.master_url, data={'cc': self.total_cc})


def main():

    print("Worker is ready to receive...")
    worker = Worker()
    print("URL list received...")
    worker.receive_work()

if __name__ == "__main__":
    main()