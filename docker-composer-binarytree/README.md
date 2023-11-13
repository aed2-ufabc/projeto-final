# Docker Compose

There are two types os services:

**main:** this is a python service with ftp connection capabilities

**remotes:** this is a ftp service. The files of each remote are in the folder named files.

## Build and run

Open 2 terminal windows and run these commands:

1. Build and run the images: `docker-compose run main` 
2. Check the memory and CPU usage `docker stats`

To finish all services run `docker-compose down`

If you need to add some new lib, rebuid everything with: `docker-compose build`

