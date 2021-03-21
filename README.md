## XRDP Server for GUI in Docker Container - Works on multiple platforms including raspberry-pi

Documentation TBA

### How to run the container with XRDP:

`docker run -d -e GUEST_PASS='guest' -p 3389:3389 -v $(pwd)/home/guest:/home/guest --name xrdp satishweb/xrdp`

Connect to the container using the remote desktop client on localhost:3389 and login with user guest and password as guest

### Note:- This is still a work in progress.

### Planned features:
- Build container image as soon as a new stable version of xrdp is released.
- Add container images for other popular distros.
- Automated tests of newly built container image with CI pipeline (I have free infrastructure resources).
- Add more configuration options for the container image.
- Link container image tag versions to the XRDP version inside the image.
