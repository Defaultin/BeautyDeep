import os
import dlib
from keras.backend import tf as ktf
from keras.models import Sequential
from keras.layers import Dense
from keras.applications.resnet50 import ResNet50

__all__ = ('BeautyDeepNet')


APP_ROOT = os.path.abspath('')


def BeautyDeepNet():
	detector_path = APP_ROOT + '/cnn-config/mmod_human_face_detector.dat'
	predictor_path = APP_ROOT + '/cnn-config/shape_predictor_68_face_landmarks.dat'
	detector = dlib.cnn_face_detection_model_v1(detector_path)
	predictor = dlib.shape_predictor(predictor_path)

	resnet = ResNet50(include_top=False, pooling='avg')
	model = Sequential()
	model.add(resnet)
	model.add(Dense(5, activation='softmax'))
	model.layers[0].trainable = False
	model.load_weights(APP_ROOT + '/cnn-config/BeautyDeep-Net.h5')
	global graph
	graph = ktf.get_default_graph()

	return graph, model, detector, predictor