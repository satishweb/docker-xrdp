## XRDP Server for GUI in Docker Container

This is a Linux development environment running under Docker that works
on Apple Silicon.

Forked from [satishweb/docker-xrdp](https://github.com/satishweb/docker-xrdp).
Upgraded Ubuntu, added some more basic dev tools, especially for Python.

### Building

Standard docker build:

`docker build -t jooray/xrdp .`

On OSX on Apple Silicon, you need to run:

`docker buildx build --platform=linux/amd64 -t jooray/xrdp .`

### How to run the container with XRDP:

`docker run -d -e GUEST_PASS='guest' -p 3389:3389 -v $(pwd)/home/guest:/home/guest --name xrdp jooray/xrdp`

Connect to the container using the remote desktop client on localhost:3389 and login with user guest and password guest
