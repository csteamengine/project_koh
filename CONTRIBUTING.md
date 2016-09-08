# Contributing

## Install PyCharm by Jetbrains
  - [Install](https://www.jetbrains.com/pycharm/download/)

## Download Python 3
  - [Download](https://www.python.org/downloads/)
  - Make sure to install Python 3.5.2!

## Install tornado python API
  - [Install](http://www.tornadoweb.org/en/stable/index.html)
  - Make sure to install the python3 version of tornado
  - The following will install tornado with python3 on linux and mac (May have to install pip first)
  ```
  sudo python3 -m pip install tornado
  ```
  - or
  ```
  pip3 install tornado
  ```
  - on windows, may have to follow the manual installation on the site.

## Set Up Python Server
  - Navigate to File | Settings | Project: se329_project_1 | Project Interpreter
  - Click to create a new local project interpreter direct it to the python 3.5 download location
    - (/usr/local/bin/python3.5) for mac
    - (/User/Brody/AppData/Local/Programs/Python/Python35-32/python.exe) for windows
  - Save interpreter and exit settings

## Set up Server 
  - Navigate to Run | Edit Configurations
  - Click the '+' icon in the top right and select 'Python'
  - Point the script to our server script 'server/server.py'
  - Make sure the interpreter is pointing to the python3.5 interpreter we created in the previous step
  - Name the server something. (Ex// Server 8888)

## Launch 
  - The server must now be started in the terminal by typing 
  ```
  python3 server.py
  ```
  - Navigate to localhost:8888 in browser
  
## Changes
  - When you change anything, you will need to restart the server by clicking the restart button
  - Then you can go to the browser and reload the page.
  


