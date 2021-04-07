# BeautyDeep

BeautyDeep is an app which evaluates the beauty of a human face from a photo given. The system itself recognizes one or several faces on the photo and evaluates the percentage of their beauty, also analysing each person’s character according to their face features. 

The program uses a neural network trained to evaluate the beauty percentage on the basis of more than 10 thousand [photos](https://github.com/HCIILAB/SCUT-FBP5500-Database-Release) already rated by real people, and also detectors recognising the features of the face. Using mathematical formulas the face features are typified, each of the types describing the person’s character according to neurotypology laws.

![](https://github.com/Defaultin/BeautyDeep/blob/master/mobile-app/images/logo-bg.png "BeautyDeep")
<img src="https://github.com/Defaultin/BeautyDeep/blob/master/papers/app-preview.gif" width="270" height="480" />

# Repository structure

* mobile-app -- source code of an android mobile application
* neural-network -- source code for training and testing the neural network
* web-server -- source code of a flask web application
* papers -- pdf documents with project documentation
* app-preview.mov -- video-preview of a mobile application powered by android 8

# Dependencies

```bash
$ pip install -r BeautyDeep/mobile-app/requirements.txt
$ pip install -r BeautyDeep/neural-network/requirements.txt
$ pip install -r BeautyDeep/web-server/requirements.txt
```

# How to use

## For local server

1. Install all dependencies for application and server
2. Connect your phone and computer devices to the same network
3. Open "BeautyDeep/web-server" and start the [server.py](https://github.com/Defaultin/BeautyDeep/blob/master/web-server/server.py)
4. Wait until the neural network configurations are loaded
5. Install the mobile [application](https://drive.google.com/uc?export=download&id=1FpxAb0mg5gEAKXC7Pxw6q5OkXrXsylHQ) or open "BeautyDeep/mobile-app" on your computer and run [main.py](https://github.com/Defaultin/BeautyDeep/blob/master/mobile-app/main.py)
6. In the server settings of the application, specify the public ip address (e.g. http://192.168.0.102:5000) of your local machine

## For remote server

1. Deploy the web application to the remote server or run [setup.sh](https://github.com/Defaultin/BeautyDeep/blob/master/web-server/setup.sh) on your remote PowerShell
2. Install the mobile [application](https://drive.google.com/uc?export=download&id=1FpxAb0mg5gEAKXC7Pxw6q5OkXrXsylHQ) or open "BeautyDeep/mobile-app" on your computer and run [main.py](https://github.com/Defaultin/BeautyDeep/blob/master/mobile-app/main.py)
3. In the server settings of the application, specify the domain (e.g. http://domain.io) or public ip address (e.g. http://34.91.143.244:5000) of your remote server
