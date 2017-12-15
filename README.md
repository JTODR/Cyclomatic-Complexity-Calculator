# Python Cyclomatic Complexity Calculator
# CS4400 Internet Applications Assignment
**Name:** Joseph O'Donovan  
**Student Number:** 14315530

## Dependencies
This project is written in **Python 3.6**  
It was written on a Windows Machine and it **must be run on a Windows machine** due to the command prompt script to start the workers.
Python's Flask, requests and radon modules are needed to run the manager and the worker, use a virtualenv to install them.

To run this project, do the following:

1. **This bit is important!** In GitHub, go to: Settings -> Developer Settings -> Personal access tokens -> Generate new token -> Enter password -> Generate token. Then copy the generated token to the clipboard. In the working directory of the manager and the worker, open a text file and name it 'github-token.txt'. Paste the generated token into this text file. The manager and worker will use this token to access the GitHub API.
2. Run the manager: **python manager.py [number of workers]**
3. Once the Manager's Flask server is running, run the run_workers.cmd script to start the workers: **run_workers.cmd [number of workers]**


## Project Overview
This project calculates the cyclomatic complexity of all python files in a given github repository. The basis of the project is that the worker applications are always looking for work to do and the manager allocates the work to the workers. There is one manager for N workers. The manager distributes the work and receives the cyclomatic complexity for each batch of work (batch of files). The manager then averages the cyclomatic complexity for all files in the repository, outputting the result.

----

**Manager**

The manager uses the github API to obtain files from the respository. It is given a URL to the commits of a repo (for example: https://api.github.com/repos/JTODR/Cyclomatic-Complexity-Calculator/commits) and from there it obtains the blob file URL's. The manager uses python's requests module to get the URL and it parses out the file tree of each commit. For each file tree it obtains the blob URLs of all files in the tree. It then sends the blob URLs to a Flask server. The manager receives the cyclomatic complexity of each batch of files that the worker works on. It then averages this complexity for the repository.


----

**Worker**

Upon reception of a blob URL the worker parses out the URL and the filename from the URL. It then checks if the file is a python file. If so, it uses python's requests module to retrieve the contents of the file. It then writes the contents to a temporary local file. It reads in this file and uses CCHarvester from python's radon module to determine the complexity of the file. This returns the complexity of each section of code in the file. The worker appends this to a total complexity for the file and sends the result back to the manager via the Flask server.

The CCHarvester class is defined here: https://github.com/rubik/radon/blob/master/radon/cli/harvest.py