# Funicular.js
Kinect to JS communication using Python with WebSockets.
### Dependencies
- Kinect Sensor v1
- [OpenNI](https://github.com/OpenNI/OpenNI)
- [PyOpenNI](https://github.com/jmendeth/PyOpenNI)
- [Tornado](http://www.tornadoweb.org/en/stable/)
- Local webserver: eg [MAMP](link:http://www.mamp.info/en/), [XAMPP](https://www.apachefriends.org/index.html)

### Setting Dependencies Up
1. Install [OpenNI](https://github.com/OpenNI/OpenNI). Some instructions for the installation for this are [here.](http://justinfx.com/2012/06/21/getting-started-with-xbox-360-kinect-on-osx/)
2. Next, you should install [PyOpenNI](https://github.com/jmendeth/PyOpenNI). Be sure to copy the generated `lib/openni.<ext>` to your Python modules directory. Ensure it has installed correctly by running some of [PyOpenNI](https://github.com/jmendeth/PyOpenNI) demos to ensure that the Kinect sensor is communicating with Python.
3. Next, Tornado should be downloaded and installed from the [website.](http://www.tornadoweb.org/en/stable/)

### Getting Started
1. Clone the Funicular.js repo to your local webserver.
```
git clone git@github.com:adeniszczyc/Funicular.js.git
```
2. Ensure your Kinect is plugged into USB and connected to a power source.
3. From Terminal, run the Python websocket file
```
$ python server.py
```
4. In your browser navigate to the client demo webpage. Be sure to do this through the webserver.
5. Wave furiously at the Kinect, and you should see the hand tracking working.

### Credits
- [Andrew Deniszczyc](http://andrewdeniszczyc.com) - [Funicular.js](https://github.com/adeniszczyc/Funicular.js)
- [DepthJS](http://depthjs.media.mit.edu/) for inspiration for this project. 
- [Robert Deniszczyc](http://builtbyrobert.com) for the name.
