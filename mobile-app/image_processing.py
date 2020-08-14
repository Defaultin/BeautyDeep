import os
import cv2
import json
import requests
from face_params import Face


__all__ = ('Image')
	

class Image:
	'''Image with marked faces and landmarks'''
	def __init__(self, path):
		self.path = path
		self.name = os.path.basename(path)
		self.output_name = 'output_' + self.name
		self.count = 0
		self.faces = []
		self.image = self.load_image()

	def load_image(self):
		'''Resizes given image for CNN inputs'''
		im = cv2.imread(self.path)
		if im.shape[0] > 1280:
			new_shape = (1280, im.shape[1] * 1280 / im.shape[0])
		elif im.shape[1] > 1280:
			new_shape = (im.shape[0] * 1280 / im.shape[1], 1280)
		elif im.shape[0] < 640 or im.shape[1] < 640:
			new_shape = (im.shape[0] * 2, im.shape[1] * 2)
		else:
			new_shape = im.shape[0:2]

		return cv2.resize(im, (int(new_shape[1]), int(new_shape[0])))

	def create_output(self, *, mask=False):
		'''Highlights faces and landmarks on the image'''
		im = self.image
		for idx, obj in enumerate(self.faces):
			if mask:
				for (x, y) in obj.shape:
					cv2.circle(im, (x, y), 1, (255, 0, 0), 2)

			cv2.rectangle(im, (obj.face[0], obj.face[1]), (obj.face[2], obj.face[3]), (0, 255, 0), 3)
			cv2.putText(im, f'Face {idx+1}', (obj.face[0], obj.face[3] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
		if mask:
			cv2.imwrite('mask-output.jpg', im)
		else:
			cv2.imwrite('output.jpg', im)

	def send_request(self, *, server='http://192.168.0.102:5000'):
		'''Sends an image to a remote server for neural network processing'''
		url = server + '/face_detection'
		headers = {'content-type': 'image/jpeg'}
		_, encoded_image = cv2.imencode('.jpg', self.image)
		response = requests.post(url, data=encoded_image.tostring(), headers=headers)

		faces = json.loads(response.text)['faces']
		self.count = len(faces)
		for face in faces:
			self.faces.append(Face(*face))