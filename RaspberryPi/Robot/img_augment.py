'''
This module does the following:

'''
import numpy as np
# np.set_printoptions(threshold=np.nan)
import csv
import cv2
import glob
import os, os.path
import shutil
import sys
import time


from img_filter_multiply import ImageFilterMultiplier
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from tqdm import tqdm


class ImageAugmenter(object):

    def __init__(self, n=1, sigma=0.33, timestr=None):

        # DELETE the contents of 'training_images_filtered' and start anew. This is, after all, where the results of this module get dumped.
        shutil.rmtree('./augmented')
        os.makedirs(  './augmented')

        self.blurred = None
        self.n = n
        self.sigma = sigma
        self.timestr = timestr
        self.npzfilename = 'aug_sigma{}_{}.npz'.format(str(self.sigma)[-2:], self.timestr)

        self.rotation_range = 1
        self.width_shift_range = 0.02
        self.height_shift_range = 0.02
        self.shear_range = 0
        self.zoom_range = 0.1
        self.fill_mode = 'nearest'

        # Location of original images (or image folders) collected.
        self.loc_originals_img             = './images/imgs_2019*/*.jpg'
        # self.loc_originals_img             = './images/imgs_20161024_201843/*.jpg'    #SUBSET

        # Location of filtered images after filter is applied to each original image.
        self.loc_filtered_img_storage_each = 'training_images_filtered/frame{:>05}.jpg'

        # Location of filtered images, referred to when 'multiply()' method commences, so it knows which images to multiply.
        self.loc_filtered_img_storage      = 'training_images_filtered/*.jpg'

        # Location of original label_array (to be multiplied).
        self.loc_originals_label_array     = './images/imgs_2019*/label_array_ORIGINALS*.npz'
        # self.loc_originals_label_array     = './images/imgs_20161024_201843/label_array_ORIGINALS.npz'    #SUBSET

        # Location where final npz file will be saved (after filter application and multiplication are finished).
        # self.loc_final_save                = 'training_data_temp/aug_sigma{}_{}.npz'.format(str(self.sigma)[-2:], time.strftime("%Y%m%d_%H%M%S"))

        # self.augment()


    def augment(self):
        print ('')
        print ('*** AUGMENT ***')
        print ('Generate new augmented images: Initiated')

        # Folders with original images, read them in one-by-one. They'll be in order according to the filepaths, which are ordered by timestamp.
        originals = glob.glob(self.loc_originals_img)

        print ('Generating {} augmentations for each of {} original images...'.format(self.n, len(originals)))

        datagen = ImageDataGenerator(rotation_range     = self.rotation_range,
                                     width_shift_range  = self.width_shift_range,
                                     height_shift_range = self. height_shift_range,
                                     shear_range        = self.shear_range,
                                     zoom_range         = self.zoom_range,
                                     fill_mode          = self.fill_mode)

        successes = 0
        for orig in tqdm(originals):
            # Add a copy of original to './augmented' folder before adding its augmented copies.
            shutil.copy(orig, './augmented')
            os.rename('./augmented/{}'.format(orig[-15:]), './augmented/aug_{}_{:>05}_orig.jpg'.format(orig[13:29],successes))
            successes += 1

            # For each original .jpg in folder
            img = load_img(orig)
            x = img_to_array(img)
            x = x.reshape((1,) + x.shape)

            for i in range(self.n):

                i = 0
                for batch in datagen.flow(x,
                                          batch_size=1,
                                          save_to_dir='./augmented',
                                          save_prefix='aug_{}_{:>05}'.format(orig[13:29],successes),
                                          save_format='jpg'):
                    i += 1
                    successes += 1
                    if i == 1:
                        i = 0
                        break

        print ('...complete!')

        # HACKY: Check if number of images in save_to_dir == number of successes.
        num_new_images = len([name for name in os.listdir('./augmented')])
        if successes != num_new_images:
            print ('Number of successes:'), successes
            print ('Number of augmented images:'), num_new_images
            print (successes,( '!='), num_new_images)
            print ('FAIL! Numbers don\'t match.')
            exit()

        print ('Generate new augmented images: Completed')
        print ('')
        print ('SUMMARY:')
        print ('Number of original images:', len(originals))
        print ('Number of original images + augmented images:', num_new_images)


    def log_update(self):

        row_params = [self.npzfilename, 
                      self.rotation_range, 
                      self.width_shift_range, 
                      self.height_shift_range, 
                      self.shear_range, 
                      self.zoom_range, 
                      self.fill_mode, 
                      self.sigma]

        with open('./logs/log_img_parameters.csv','a') as log:
            log_writer = csv.writer(log)
            log_writer.writerow(row_params)


if __name__ == '__main__':

    # Global variables
    # sigma: pertains to median threshold for canny filter
    # timestr: self-explanatory
    # cnn: whether to save images for CNN training
    sigma = 0.33
    timestr = time.strftime('%Y%m%d_%H%M%S')
    cnn = True

    # Variables specific to ImageAugmenter
    # 'n' is the number of copies to make of each original image. Keep in mind this will be doubled when flipped. FINAL COUNT == (n+1) * 2
    n = 1

    # ImageAugmenter(n=n, sigma=sigma, timestr=timestr)
    ImageAugmenter(n=n, sigma=sigma, timestr=timestr).augment()

    ImageFilterMultiplier(sigma=sigma, subsequent=True, augment=True, n=n, timestr=timestr, cnn=True)

    ImageAugmenter(n=n, sigma=sigma, timestr=timestr).log_update()
    exit()

