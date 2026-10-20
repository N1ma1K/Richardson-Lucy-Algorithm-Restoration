import numpy as np
from astropy.io import fits
from astropy.nddata import Cutout2D


def load_fits_data(filename, cutout_size=None, target_pos=None):
    with fits.open(filename) as hdul:
        data = hdul[0].data.astype(float)
        header = hdul[0].header.copy()

    if cutout_size is not None:
        if target_pos is None:
            target_pos = (data.shape[1]//2, data.shape[0]//2)
        cutout = Cutout2D(data, position=target_pos, size=cutout_size)
        data = cutout.data

    bkg = np.median(data)
    image = data - bkg

    return image, header
