import cv2
import os, sys
import pickle
import numpy as np
from keras.preprocessing.image import array_to_img
import random
from PIL import Image
from PIL import ImageEnhance


data_path = 'dataset/SCUT-FBP5500_v2/Images/'
rating_path = 'dataset/SCUT-FBP5500_v2/train_test_files/'
model_path = 'haarcascade_frontalface_alt.xml'
face_cascade = cv2.CascadeClassifier(model_path)


def detect_face(detector, image_path, image_name): 
    img = cv2.imread(image_path + image_name)
    resized_im = 0

    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    s = img.shape[1] // 2
    faces = detector.detectMultiScale(gray, 1.1, 5, 0, (s, s))

    if len(faces) == 1:
        face = faces[0]
        croped_im = img[face[1]:face[1] + face[3], face[0]:face[0] + face[2], :]
        resized_im = cv2.resize(croped_im, (224, 224))

    return resized_im


def random_update(img):
    img = array_to_img(img)

    # Spin
    image_rotated = img.rotate(random.random() * 30 - 30)

    # Brightness
    enh_bri = ImageEnhance.Brightness(image_rotated)
    image_brightened = enh_bri.enhance(random.random() * 0.8 + 0.6)

    # Contrast
    enh_con = ImageEnhance.Contrast(image_brightened)
    image_contrasted = enh_con.enhance(random.random() * 0.6 + 0.7)

    # Chroma
    enh_col = ImageEnhance.Color(image_contrasted)
    image_colored = enh_col.enhance(random.random() * 0.6 + 0.7)

    return np.asarray(image_colored)


def get_lable_distribution():
    lable_distribution = []

    with open(rating_path + 'All_labels.txt', 'r') as f:
        data = [line.strip().split(' ') for line in f]

    for d in data:
        image_name, score = d
        im = detect_face(face_cascade, data_path, image_name)
        if isinstance(im, np.ndarray):
            normed_im = (im - 127.5) / 127.5
            score, score_vec = float(score), [0] * 4
            int_part = round(score - 1)
            score_vec.insert(int_part, 1)
            lable_distribution.append([image_name, normed_im, score_vec, score])

    return lable_distribution


def split_data(dist, *, split_coeff=0.1):
    distribution = dist[:]
    data_split_index = int(len(distribution) - split_coeff * len(distribution))
    random.shuffle(distribution)
    test_lable_distribution = distribution[data_split_index:]
    train_lable_distribution = distribution[:data_split_index]

    for name, im, score_vec, score in train_lable_distribution:
        enhance_im = random_update(im)
        enhance_normed_im = (enhance_im - 127.5) / 127.5
        train_lable_distribution.append([name, enhance_normed_im, score_vec, score])

    random.shuffle(train_lable_distribution)
    random.shuffle(test_lable_distribution)
    pickle.dump(train_lable_distribution, open('train_lable_distribution.dat','wb'))
    pickle.dump(test_lable_distribution, open('test_lable_distribution.dat','wb'))


if __name__ == '__main__':
    dist = get_lable_distribution()
    split_data(dist)