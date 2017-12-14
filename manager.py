from socket import *
import requests
from collections import deque
import shutil
from flask import Flask
from flask_restful import Resource, Api, request
import sys
import time

app = Flask(__name__)
api = Api(app)

t0 = time.clock()
t1 = time.clock()

blob_url_list = deque()
new_cc = 0
total_cc = 0
blob_list_length = 0
recv_count = 0
num_workers = sys.argv[1]

class Master(Resource):

    def get(self):
        global blob_url_list

        if blob_url_list:
            return blob_url_list.popleft()
        else:
            return "finished"


    def put(self):
        global total_cc
        global recv_count
        global t0
        global t1

        new_cc = int(request.form['cc'])
        total_cc += new_cc

        print("RECEIVED: " + str(new_cc))
        recv_count += 1
  
        if recv_count == int(num_workers):
            ave_cc = total_cc / blob_list_length
            print("\nAverage CC: " + str(ave_cc))
            print("Total CC: " + str(total_cc) + "\n")   
            
            kill_manager()

        return '', 204


def kill_manager():

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def get_tree_urls(github_url):
    

    tree_urls = []

    payload_headers = get__params_headers()

    resp = requests.get(github_url,   params=payload_headers[0], headers=payload_headers[1])    # get the commit page of the github url

    for item in resp.json():
        tree_urls.append(item['commit']['tree']['url']) # parse out the tree URL's from the commit page

    return tree_urls


def get_blob_url_list(github_url, tree_urls):

    global blob_url_list
    global blob_list_length

    payload_headers = get__params_headers() 
    for blob_url in tree_urls:
        resp = requests.get(blob_url,   params=payload_headers[0], headers=payload_headers[1])

        tree = resp.json()['tree']

        for item in tree:
            file_url = item['url']
            filename = item['path']

            url_filename = file_url + '|' + filename
            blob_url_list.append(url_filename)

    blob_list_length = len(blob_url_list)


def get__params_headers():
    with open('github-token.txt', 'r') as tmp_file:
        token = tmp_file.read()     # get the token from a text file in current directory

    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    return (payload, headers)


def main():

    print ("Manager started...")
    
    github_url = 'https://api.github.com/repos/JTODR/Cyclomatic-Complexity-Calculator/commits'
    
    print("Getting Tree URL list...")
    tree_urls = get_tree_urls(github_url)      # get the list of tree URL's from the project's commits
    print("Tree URL list received...")
    
    print("Gettng blob URL's...")
    get_blob_url_list(github_url, tree_urls)    # get blob URLs of each tree's 
    print("Blob URL's received...")

    t0 = time.clock()
    app.run(host='localhost', port=2020, debug=False)
    t1 = time.clock()
    total = t1 - t0
    print("Total time taken was: " + str(total))

api.add_resource(Master, '/')

if __name__ == "__main__":
    main()