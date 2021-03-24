import cv2
import json
import logging
import numpy as np
from flask import Flask, request, Response
from beauty_deep_net import BeautyDeepNet


app = Flask(__name__)
graph, model, detector, predictor = BeautyDeepNet()


@app.route('/')
def hello():
	return '<h1>Welcome to BeautyDeep neural network server!</h1>'

@app.route('/face_detection', methods=['POST'])
def detection():
	nparray = np.frombuffer(request.data, np.uint8)
	img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)

	faces = []
	boxes = detector(img, 0)
		
	if len(boxes) > 0:
		for idx, box in enumerate(boxes):
			face = [
				box.rect.left(), 
				box.rect.top(),
				box.rect.right(), 
				box.rect.bottom()
			]
			shape = predictor(img, box.rect)
			full_shape = [(shape.part(i).x, shape.part(i).y) for i in range(68)]
			croped_image = img[face[1]:face[3], face[0]:face[2], :]
			resized_image = cv2.resize(croped_image, (224, 224))
			normed_image = np.array([(resized_image - 127.5) / 127.5])
			with graph.as_default():
				probability_vec = model.predict(normed_image)[0]

			beauty_score = np.dot(probability_vec, range(1, 6)) * 40 - 70
			if 0 <= beauty_score <= 100:
				detected = face, full_shape, beauty_score
			elif beauty_score > 100:
				detected = face, full_shape, 100.0
			else:
				detected = face, full_shape, 0.0
			faces.append(detected)

	return Response(response=json.dumps({'faces': faces}), status=200, mimetype='application/json')


if __name__ == '__main__':
	while True:
		try:
			app.run(host='0.0.0.0', port=5000, threaded=True)
		except Exception as e:
			logging.error(e)