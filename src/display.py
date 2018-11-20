from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

# Just shows a picture

image_file = './Bias/trial_bias_Bias_0.010_secs_2018-05-09T20-21-50_001.fits'
hdu_list = fits.open(image_file)
hdu_list.info()



image_data = hdu_list[0].data


plt.imshow(image_data, cmap='gray')
plt.colorbar()
plt.show()
