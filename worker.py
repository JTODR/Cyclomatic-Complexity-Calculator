import os
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
import requests
from time import gmtime, strftime
import os.path
from re import match
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
            token = tmp_file.read()     # get the personal access token from a text file in current directory

        payload = {'access_token': token}
        headers = {'Accept': 'application/vnd.github.v3.raw'}

        return (payload, headers)


    def check_python_file(self, filename):
        return True if match('.*\.py', filename) is not None else False         # return true if the file is a python file (CCHarvester only works on python files)

    def calc_CC(self, blob_url):

        url = blob_url.split('|')[0]        # parse out the actual file url 
        filename = blob_url.split('|')[1]       # parse out the file name from the url

        payload_headers = self.get__params_headers()

        flag = self.check_python_file(filename)      # check if file is a python file
        if flag == True:

            resp = requests.get(url,   params=payload_headers[0], headers=payload_headers[1])       # get the data from the file

            curr_time = time.clock()
            curr_time = str(curr_time)
            curr_time = curr_time.split('.')[1]
            sha = url.split('/blobs/')[1]       # give the temp file a unique name (sha + current processor time)

            file_path = sha + curr_time  + '.py'

            with open(file_path, 'w') as tmp_file:      # temporarily write out the file's data
                tmp_file.write(resp.text)
            tmp_file.close()


            CC_file_get = open(file_path, 'r')      # read in the file's data
            results = CCHarvester(file_path, self.cc_config).gobble(CC_file_get)        # calculate the CC of the temp file
            CC_file_get.close()
            os.remove(file_path)        # delete the temp file

            file_cc = 0

            for i in results:
                file_cc += int(i.complexity)        # append CC of all parts of the file to a total CC for the file

            print("Complexity of file: " + str(file_cc))

            return file_cc
        else:
            return 0        # if file is not a python file

    def receive_work(self):

        file_cc = self.calc_CC(self.blob_url)      # this is called on first url
        self.total_cc += file_cc

        self.blob_url = requests.get(self.manager_url).json()   # this is for all subsequent urls
        while self.blob_url != "finished":          # check for finished string on the server
            file_cc = self.calc_CC(self.blob_url)
            self.total_cc += file_cc
            self.blob_url = requests.get(self.manager_url).json()       # keep getting file urls until finish string


        print("Finished...") 
        print("Total CC: " + str(self.total_cc))
        requests.put(self.manager_url, data={'cc': self.total_cc})      # send the manager the total CC for all file urls received

def main():

    print("Worker is ready to receive...")
    worker = Worker()
    worker.receive_work()

if __name__ == "__main__":
    main()