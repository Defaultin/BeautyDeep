import pickle
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.applications.resnet50 import ResNet50
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping


def tarin_model(*, plot=False, init_weights=False):
    lable_distribution = pickle.load(open('train_lable_distribution.dat','rb'))
    train_X = np.array([x[1] for x in lable_distribution])
    train_Y = np.array([x[2] for x in lable_distribution])

    resnet = ResNet50(include_top=False, pooling='avg')
    model = Sequential()
    model.add(resnet)
    model.add(Dropout(0.5))
    model.add(Dense(5, activation='softmax'))
    model.layers[0].trainable = False
    #print(model.summary())

    if init_weights:
        model.load_weights('model-resnet-base.h5')

    sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='kld', optimizer=sgd, metrics=['accuracy'])
    earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='auto')
    history = model.fit(x=train_X, y=train_Y, batch_size=32, callbacks=[earlyStopping], epochs=100, verbose=1, validation_split=0.1)
    model.save_weights('beauty-deep-model.h5')

    if plot:
        fig = plt.figure()
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        fig.savefig('model_accuracy.png')

        fig = plt.figure()
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        fig.savefig('model_loss.png')


if __name__ == '__main__':
    tarin_model(plot=True, init_weights=True)