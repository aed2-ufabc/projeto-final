# Go
## Build and run

1. Build the image: `docker build -t myapp .`
2. Run it! `docker run -t -p 5000:5000 --memory=6m --memory-swap=7m myapp`
3. In another terminal window you can check the memory usage `docker stats`
