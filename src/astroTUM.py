import os
import astropy.nddata as nd
import astropy.io as aio
import scipy.signal as signal

import numpy as np

import matplotlib.pyplot as plt

### CAREFUL: IT DOES NOT WORK PROPERLY
### UNCOMMENTED AND HORRIBLE. 

def load_fits(path : str):
    '''Load fits file from given path'''
    return aio.fits.open(path)[0]

def mean_from_folder(path : str, image_base=None) -> np.ndarray:
    fits_list = sorted([x for x in os.listdir(path) if x.lower().endswith('.fits')])
    master_key = fits_list[0]

    fits_dict = {}
    for ifits in fits_list:
        fits_dict[ifits] = load_fits(os.path.join(path, ifits))

    if image_base is not None and \
       fits_dict[master_key].shape != image_base.data.shape:
        print("Image base has different size")
        return None

    fits_data_array = np.zeros((fits_dict[master_key].data.shape[0],
                                fits_dict[master_key].data.shape[1],
                                len(fits_list)))

    for i,ifits in enumerate(fits_list):
        if image_base is None:
            fits_data_array[:,:,i] = fits_dict[ifits].data/fits_dict[ifits].data.max()
        else:
            fits_data_array[:,:,i] = fits_dict[ifits].data/fits_dict[ifits].data.max() \
                - image_base.data

    fits_data_mean = np.mean(fits_data_array, axis=2)
    fits_data_mean -= fits_data_mean.min()
    return fits_data_mean/fits_data_mean.max()

def process_root(root_dir : str):
    dark_data_mean = mean_from_folder(os.path.join(root_dir, 'Dark'))
    dark_ccd = nd.CCDData(data=dark_data_mean, unit="adu")
    flat_data_mean = mean_from_folder(os.path.join(root_dir, 'Flat'),
                                      image_base=dark_ccd)
    flat_ccd = nd.CCDData(data=flat_data_mean, unit="adu")
    light_data_mean = mean_from_folder(os.path.join(root_dir, 'Light'),
                                       image_base=flat_ccd)
    light_ccd = nd.CCDData(data=light_data_mean, unit="adu")
    return light_ccd

def cut_fits(fits, x_offset, y_offset, width, height):
    """Returns an updated cut version of the fits file"""
    if width is None:
        width = len(fits.data)-x_offset
    if height is None:
        height = len(fits.data)-y_offset
    fits.data = fits.data[x_offset:width, y_offset:height]
    fits.header['NAXIS1'] = width
    fits.header['NAXIS2'] = height

    return fits


#root_dir = '/home/pedro/Projects/PYTHON/astro/18_10_17/'
#root_ccd = process_root(root_dir)

root_dir = '/home/pedro/Projects/PYTHON/astro/18_10_17/moon_fast/'
root_ccd = nd.CCDData(data=mean_from_folder(os.path.join(root_dir, 'Light')), unit="adu")
nd.fits_ccddata_writer(root_ccd, os.path.join(root_dir, "processed.fits"))


#nebula = nd.Cutout2D(nebula_ccd, (950, 1500), (300, 300))

#plt.imshow(np.log(nebula.data))
#plt.show()
