# Docker Compose

## Build and run

Open 3 terminal windows and run these commands:

1. Build and run the images: `docker-compose up`
2. Check the memory and CPU usage `docker stats`
3. Run the main service! `docker-compose exec main /venv/bin/python3 app.py`

If you put 'a' it will call the remote1, if you put 'b' it will call the remote2. Anything diferent will call remote1 and it will return a 404 error