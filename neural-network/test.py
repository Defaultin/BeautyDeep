from keras.models import Sequential
from keras.layers import Dense
from keras.applications.resnet50 import ResNet50
import cv2
import pickle
import numpy as np
import matplotlib.pyplot as plt


score = []
pred_score = []

resnet = ResNet50(include_top=False, pooling='avg')
model = Sequential()
model.add(resnet)
model.add(Dense(5, activation='softmax'))
model.layers[0].trainable = False
model.load_weights('beauty-deep-model.h5')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
test_lable_distribution_data = pickle.load(open('test_lable_distribution.dat','rb'))
test_lable_distribution = train_Y = [x for x in test_lable_distribution_data] 

for i in range(len(test_lable_distribution_data)):
    label_distribution = test_lable_distribution[i]
    image = label_distribution[1]
    label_score = label_distribution[3]
    score.append(label_score)
    pred = model.predict(np.expand_dims(image, axis=0))
    predict = sum((i+1) * pred[0][i] for i in range(5))
    pred_score.append(predict)

    print(f'Name: {str(label_distribution[0])}')
    print('Score: %1.2f' % (label_score))
    print(f'Predict: {str(predict)}')

Y = np.asarray(score)
X = np.asarray(pred_score)
pc = np.corrcoef(Y, X)[0,1]
print('Pearson correlation = %1.2f' % (pc))

fig = plt.figure()
plt.scatter(Y, X)
plt.title('Pearson correlation = %1.2f' % (pc))
plt.ylabel('labels')
plt.xlabel('predicts')
fig.savefig('correlation.png')