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

    master_url = 'http://localhost:2020/'
    node_setup_url = 'http://localhost:2020/init'

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
        self.files_list_url = requests.get(self.master_url).json()#['url']
        print(self.files_list_url)

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
                print (i.complexity)
                file_cc += int(i.complexity)

            #avg_cc = file_cc/ len(results)
            print("Complexity of file: " + str(file_cc))
            #print("Average complexity of file: " + str(avg_cc))
            return file_cc
        else:
            return -1

    def receive_work(self):

        total_cc = 0
        for blob_url in self.files_list_url:
            print("Blob is: " + blob_url)

            file_cc = self.calc_CC(blob_url)
            total_cc += file_cc
            print(str(file_cc))


        print("Finished...") 
        print("Total CC is " + str(total_cc)) 


def main():

    print("Worker is ready to receive...")
    worker = Worker()
    print("URL list received...")
    worker.receive_work()

if __name__ == "__main__":
    main()