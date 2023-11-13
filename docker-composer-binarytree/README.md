# Docker Compose

There are two types os services:

**main:** this is a python service with ftp connection capabilities

**remotes:** this is a ftp service. The files of each remote are in the folder named files.

## Build and run

Open 2 terminal windows and run these commands:

1. Build and run the images: `docker-compose run main` 
2. Check the memory and CPU usage `docker stats`

If you put a word that starts with 'a' it will call the remote1, if starts with 'b' it will call the remote2 and if starts with  'c'it will call remote3. Anything with a different start will call remote3 and it will return a error.

To finish all services run `docker-compose down`

If you need to add some new lib, rebuid everything with: `docker-compose build`

