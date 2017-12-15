import requests
from collections import deque
from flask import Flask
from flask_restful import Resource, Api, request
import sys
import time

app = Flask(__name__)
api = Api(app)

t0 = time.clock()  
t1 = time.clock()

blob_url_list = deque()
worker_cc = 0           # CC received from a worker
total_cc = 0            # total CC of all worker_cc's
avg_cc = 0              # average CC for all commits
blob_list_length = 0
recv_count = 0
num_workers = sys.argv[1] 

class Manager(Resource):

    def get(self):
        global blob_url_list
        global t0

        if blob_url_list:
            if blob_list_length-1 == len(blob_url_list):    # record intial time when first url is taken by a worker
                t0 = time.clock()
            return blob_url_list.popleft()
        else:
            return "finished"   # when all urls are complete


    def put(self):
        global total_cc
        global recv_count
        global t0
        global t1
        global ave_cc

        worker_cc = int(request.form['cc'])     # receive result from a worker
        total_cc += worker_cc           # append to total CC of commits

        print("RECEIVED: " + str(worker_cc))
        recv_count += 1
  
        if recv_count == int(num_workers):
            kill_manager()          # end the server if number of received results = number of workers
                
        return '', 204


def kill_manager():

    func = request.environ.get('werkzeug.server.shutdown')      # shut down the server
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def get_tree_urls(github_url):

    tree_urls = []

    payload_headers = get_params_headers()

    resp = requests.get(github_url,   params=payload_headers[0], headers=payload_headers[1])    # get the commit page of the github url

    for item in resp.json():
        tree_urls.append(item['commit']['tree']['url']) # parse out all tree URLs from the commit page and append to a list

    return tree_urls


def get_blob_url_list(tree_urls):

    global blob_url_list
    global blob_list_length

    payload_headers = get_params_headers() 

    for blob_url in tree_urls:
        resp = requests.get(blob_url,   params=payload_headers[0], headers=payload_headers[1])  # get data at each tree url

        tree = resp.json()['tree']

        for item in tree:
            file_url = item['url']      # parse out the url of each file in the tree
            filename = item['path']     # parse out the file name of each file in the tree

            url_filename = file_url + '|' + filename
            blob_url_list.append(url_filename)      # append the two to the blob list - these will be sent to the flask server

    blob_list_length = len(blob_url_list)   # record the length of the list 


def get_params_headers():
    with open('github-token.txt', 'r') as tmp_file:
        token = tmp_file.read()     # get the personal access token from a text file in current directory

    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    return (payload, headers)


def main():

    print ("Manager started...")
    
    # Url of the project is: https://github.com/JTODR/Cyclomatic-Complexity-Calculator
    github_url = 'https://api.github.com/repos/JTODR/Cyclomatic-Complexity-Calculator/commits'  # commit url of this project on github 
    
    print("Getting Tree URL list...")
    tree_urls = get_tree_urls(github_url)      # get the list of tree URLs from the project's commits
    print("Tree URL list received...")
    
    print("Gettng blob URL's...")
    get_blob_url_list(tree_urls)    # get blob URLs of each tree 
    print("Blob URL's received...")

    app.run(host='localhost', port=2020, debug=False)       # start the flask server
    t1 = time.clock()               # record the end time after server has shut down

    ave_cc = total_cc / blob_list_length        # get average CC for all commits
    print("\nAverage CC: " + str(ave_cc))
    print("Total CC: " + str(total_cc) + "\n")

    total = t1 - t0
    print("Total time taken was: " + str(total) + " seconds")

    time_str = "num_workers=" + str(num_workers) + ", time=" + str(total) + "sec\n"

    with open("WorkerTime.txt", 'a+') as time_file:     # write the time taken to a text file
        time_file.write(time_str)
    

api.add_resource(Manager, '/')

if __name__ == "__main__":
    main()