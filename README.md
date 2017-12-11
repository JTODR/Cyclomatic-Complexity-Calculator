# Python Cyclomatic Complexity Calculator
# CS4400 Internet Applications Assignment
**Name:** Joseph O'Donovan  
**Student Number:** 14315530

## Dependencies
This project is written in **Python 3.6**  
It was written on a Windows Machine.

To run this project, do the following:

* Run the worker: **python worker.py**
* Then, run the manager: **python manager.py**


## Project Overview
This project calculates the cyclomatic complexity of all python files in a given github repository. The basis of the project is that the worker application is always looking for work to do and the manager allocates the work to the worker. There is one manager for N workers. The manager distributes the work and receives the cyclomatic complexity for each file. The manager then averages the cyclomatic complexity for all files in the repository. 

----

**Manager**

The manager uses the github API to obtain files from the respository. It is given a URL to the commits of a repo and from there it obtains the file. The URL will look like this: https://api.github.com/repos/JTODR/Cyclomatic-Complexity-Calculator/commits

The manager uses python's requests module to get the URL and it parses out the file tree of each commit. For each file tree it obtains the blob URLs of all files in the tree. It then sends the list of blob URLs to the worker. The manager receives the cyclomatic complexity of each blob URL sent to the worker. It then averages this complexity for the repository.


----

**Worker**

Upon reception of a blob URL the worker parses out the URL and the filename from the URL. It then checks if the file is a python file. If so, it uses python's requests module to retrieve the contents of the file. It then writes the contents to a temporary local file. It reads in this file and uses CCHarvester from python's radon module to determine the complexity of the file. This returns the complexity of each section of code in the file. The worker appends this to a total complexity for the file and sends the result back to the manager. 

The CCHarvester class is defined here: https://github.com/rubik/radon/blob/master/radon/cli/harvest.py