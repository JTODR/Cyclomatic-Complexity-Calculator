from socket import *
import requests
from collections import deque
import shutil

def get_tree_urls(github_url):
    

    tree_urls = []

    payload_headers = get__params_headers()

    resp = requests.get(github_url,   params=payload_headers[0], headers=payload_headers[1])    # get the commit page of the github url

    for item in resp.json():
        tree_urls.append(item['commit']['tree']['url']) # parse out the tree URL's from the commit page

    return tree_urls


def get_blob_url_list(github_url, tree_urls):

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

def get__params_headers():
    with open('github-token.txt', 'r') as tmp_file:
        token = tmp_file.read()     # get the token from a text file in current directory

    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}

    #print(token)
    return (payload, headers)

def send_work(blob_url_list):
    serverName = 'localhost'
    serverPort = 1598
    total_cc = 0

    count = 0

    # send URL's one by one to the worker
    for blob_url in blob_url_list:  
        manager_socket = socket(AF_INET, SOCK_STREAM)
        manager_socket.connect((serverName,serverPort))
        manager_socket.send(blob_url.encode())      
        print("SENT: " + blob_url)

        reply = manager_socket.recv(1024)   # receive the cyclomatic complexity for the file at the current raw URL
        reply = reply.decode()
        print("RECEIVED: " + reply)

        if reply != "-1" and reply is not None:
            reply = int(reply)
            total_cc += reply       # increment total commit CC with the reply from the worker
            count += 1
        manager_socket.close()
    print ("Count = " + str(count))
    return total_cc

def main():

    github_url = 'https://api.github.com/repos/JTODR/Cyclomatic-Complexity-Calculator/commits'
   
    print("Getting SHA list...")
    tree_urls = get_tree_urls(github_url)      # get the list of tree URL's from the project's commits
    print("SHA list received...")
    print("Gettng raw URL's...")
    blob_url_list = get_blob_url_list(github_url, tree_urls)    # get blob URLs of each tree's 
    #print (raw_url_list)
    #blob_url_list = ['https://api.github.com/repos/geekcomputers/Python/git/blobs/b92c525955a1a4ef80cfad2564db957d78716996|4 Digit Number Combinations.py', 'https://api.github.com/repos/geekcomputers/Python/git/blobs/90ba62afc956f576c5832d571a4c85188d817fac|CountMillionCharacter.py', 'https://api.github.com/repos/geekcomputers/Python/git/blobs/47482ba68585483023372e3999e1927ac25c7991|CountMillionCharacters-2.0.py', 'https://api.github.com/repos/geekcomputers/Python/git/trees/273f0bab9e233ec1769be11c3125cecc15c7af93|CountMillionCharacters-Variations', 'https://api.github.com/repos/geekcomputers/Python/git/blobs/5d8c91b96191295eeb110c1dad5ecdc0514bad98|Cricket_score.py', 'https://api.github.com/repos/geekcomputers/Python/git/blobs/dbdc0aa1c88b1c67359abe18c362fb787729ab26|EncryptionTool.py', 'https://api.github.com/repos/geekcomputers/Python/git/trees/7883cb00218da1977239da0ef38c624511bc1c86|Google Image Downloader', 'https://api.github.com/repos/geekcomputers/Python/git/blobs/35fed53df4c43da9e63df6632ccac45c5ace72ee|Google_News.py', 'https://api.github.com/repos/geekcomputers/Python/git/blobs/586686d066848def5d273599180e54f23cca2170|GroupSms_Way2.py']
    print("Commenced sending of raw URL's to worker...")
    total_cc = send_work(blob_url_list)     # send the raw URL's to the worker

    print("Total CC is: " + str(total_cc))  

    avg_cc = total_cc/len(blob_url_list)
    print("Average CC is: " + str(avg_cc))

if __name__ == "__main__":
    main()