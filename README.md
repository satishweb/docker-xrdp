## XRDP Server for GUI in Docker Container - Works on multiple platforms including raspberry-pi

### How to run the container with XRDP:

`docker run -d -e GUEST_PASS='guest' -p 3389:3389 -v $(pwd)/home/guest:/home/guest --name xrdp satishweb/xrdp`

Connect to the container using the remote desktop client on localhost:3389 and login with user guest and password as guest
