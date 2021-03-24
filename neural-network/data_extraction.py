import zipfile
import pandas
import os


def extract(*, data='data.zip'):
    with zipfile.ZipFile(data, 'r') as zip_ref:
        zip_ref.extractall('dataset')

    dataset = 'dataset/SCUT-FBP5500_v2/'
    ratings_file = pandas.read_excel('dataset/SCUT-FBP5500_v2/All_Ratings.xlsx')

    cf = ratings_file.Filename.str.startswith('CF')
    cm = ratings_file.Filename.str.startswith('CM')
    af = ratings_file.Filename.str.startswith('AF')
    am = ratings_file.Filename.str.startswith('AM')

    dfcf = ratings_file[cf]
    dfcm = ratings_file[cm]
    dfaf = ratings_file[af]
    dfam = ratings_file[am]

    dfcf.to_csv(os.path.join(dataset, 'caucasian_female_images.csv'), header=False, index_label=False)
    dfcm.to_csv(os.path.join(dataset, 'caucasian_male_images.csv'), header=False, index_label=False)
    dfaf.to_csv(os.path.join(dataset, 'asian_female_images.csv'), header=False, index_label=False)
    dfam.to_csv(os.path.join(dataset, 'asian_male_images.csv'), header=False, index_label=False)


if __name__ == '__main__':
    extract()