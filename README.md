# BeautyDeep

BeautyDeep is an app which evaluates the beauty of a human face from a photo given. The system itself recognizes one or several faces on the photo and evaluates the percentage of their beauty, also analysing each person’s character according to their face features. 

The program uses a neural network trained to evaluate the beauty percentage on the basis of more than 10 thousand [photos](https://github.com/HCIILAB/SCUT-FBP5500-Database-Release) already rated by real people, and also detectors recognising the features of the face. Using mathematical formulas the face features are typified, each of the types describing the person’s character according to neurotypology laws.

![alt text](https://github.com/Defaultin/BeautyDeep/blob/master/mobile-app/images/logo-bg.png "BeautyDeep")

# Server dependencies

* Python 3.x
* Tensorflow 1.14.0
* Keras 2.2.4
* Opencv 4.1.1
* Numpy
* Dlib
* Json
* Flask
* Logging

# App dependencies

* Python 3.x
* hostpython 3.x
* Kivy
* Plyer
* Kivymd
* Akivymd
* Numpy
* Socket
* Requests
* Json
* Openssl
* Opencv

# How to use

1. Connect your phone and computer devices to the same network
2. Open "BeautyDeep/web-server" and start the [server.py](https://github.com/Defaultin/BeautyDeep/blob/master/web-server/server.py)
3. Wait until the neural network configurations are loaded
4. Install the mobile [application](https://drive.google.com/uc?export=download&id=1W6_wr7gvIHK6yud1tDzUHIYLGwO01PiA) or open "BeautyDeep/mobile-app" on your computer and run [main.py](https://github.com/Defaultin/BeautyDeep/blob/master/mobile-app/main.py)
