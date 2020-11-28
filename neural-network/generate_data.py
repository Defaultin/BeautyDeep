import cv2
import os, sys
import pickle
import numpy as np
from keras.preprocessing.image import array_to_img
import random
from PIL import Image
from PIL import ImageEnhance


data_path = 'dataset/SCUT-FBP5500_v2/Images/'
rating_path = 'dataset/SCUT-FBP5500_v2/'
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
    pre_vote_image_name = ''
    pre_vote_image_score1_cnt = 0
    pre_vote_image_score2_cnt = 0
    pre_vote_image_score3_cnt = 0
    pre_vote_image_score4_cnt = 0
    pre_vote_image_score5_cnt = 0
    rating_files = ['caucasian_female_images.csv', 
                    'caucasian_male_images.csv', 
                    'asian_female_images.csv', 
                    'asian_male_images.csv']

    for rating_file_name in rating_files:
        rating_file = open(rating_path + rating_file_name, 'r')
        lines = rating_file.readlines()
        lines.pop(0)
        lineIdx = 0

        for line in lines:
            line = line.strip().split(',')
            lineIdx += 1;
            curr_row_image_name = line[2]
            score = int(line[3])

            if pre_vote_image_name == '':
                pre_vote_image_name = curr_row_image_name

            if (curr_row_image_name != pre_vote_image_name) or (lineIdx == len(lines)):
                total_vote_cnt = pre_vote_image_score1_cnt + pre_vote_image_score2_cnt + pre_vote_image_score3_cnt + pre_vote_image_score4_cnt + pre_vote_image_score5_cnt
                score1_ld = pre_vote_image_score1_cnt / total_vote_cnt
                score2_ld = pre_vote_image_score2_cnt / total_vote_cnt
                score3_ld = pre_vote_image_score3_cnt / total_vote_cnt
                score4_ld = pre_vote_image_score4_cnt / total_vote_cnt
                score5_ld = pre_vote_image_score5_cnt / total_vote_cnt

                im = detect_face(face_cascade, data_path, pre_vote_image_name)

                if isinstance(im, np.ndarray):
                    normed_im = (im - 127.5) / 127.5
                    ld = []
                    ld.append(score1_ld)
                    ld.append(score2_ld)
                    ld.append(score3_ld)
                    ld.append(score4_ld)
                    ld.append(score5_ld)
                    lable_distribution.append([pre_vote_image_name, normed_im, ld])

                pre_vote_image_name = curr_row_image_name
                pre_vote_image_score1_cnt = 0
                pre_vote_image_score2_cnt = 0
                pre_vote_image_score3_cnt = 0
                pre_vote_image_score4_cnt = 0
                pre_vote_image_score5_cnt = 0

            if score == 1:
                pre_vote_image_score1_cnt += 1
            elif score == 2:
                pre_vote_image_score2_cnt += 1
            elif score == 3:
                pre_vote_image_score3_cnt += 1
            elif score == 4:
                pre_vote_image_score4_cnt += 1
            elif score ==5:
                pre_vote_image_score5_cnt += 1

        rating_file.close()

    return lable_distribution


def split_data(dist, *, split_coeff=0.1):
    distribution = dist[:]
    data_split_index = int(len(distribution) - split_coeff * len(distribution))
    random.shuffle(distribution)
    test_lable_distribution = distribution[data_split_index:]
    train_lable_distribution = distribution[:data_split_index]

    for i in range(len(train_lable_distribution)):
        im = train_lable_distribution[i][1]
        enhance_im = random_update(im)
        enhance_normed_im = (enhance_im - 127.5) / 127.5
        train_lable_distribution.append([pre_vote_image_name, enhance_normed_im, ld])

    random.shuffle(train_lable_distribution)
    random.shuffle(test_lable_distribution)
    pickle.dump(train_lable_distribution, open('train_lable_distribution.dat','wb'))
    pickle.dump(test_lable_distribution, open('test_lable_distribution.dat','wb'))


if __name__ == '__main__':
    dist = get_lable_distribution()
    split_data(dist)