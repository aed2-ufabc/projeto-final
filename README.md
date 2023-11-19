# Algorithms and Data Structures 2 Project

This repo contains an English and Spanish dictionaries with meaning and auto corrector application. 

The main app runs inside a container with limited RAM memory and call remote files with FTP to search for similar words and meaning using a Trie Data Structure.

There are two types os containers:

**main:** this is a python service with ftp connection capabilities. This service calls the necessary data via FTP and process it using a Trie data structure.

**remotes:** this is a ftp service. The files of each remote are in the folder named files. Each remote is responsible for a part of the dictionary data.

## Build and run

Open a terminal window and run: `docker-compose run main` 

This will start firt the remotes FTPs then it will start the main application where is posible to search for words.

Open another terminal tab and run `docker stats`. To check the memory and CPU usage of each container.

To finish all services run `docker-compose down`

