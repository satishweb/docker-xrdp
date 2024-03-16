## XRDP Server for GUI in Docker Container

This is a Linux development environment running under Docker that works on
linux/amd64,linux/arm64,linux/arm/v7,linux/ppc64le platforms.

### How to run the container with XRDP:

`docker run -d -e GUEST_PASS='guest' -p 3389:3389 -v $(pwd)/home/guest:/home/guest --name xrdp satishweb/xrdp`

Connect to the container using the remote desktop client on localhost:3389 and login with user guest and password guest
