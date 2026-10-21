import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def rmse(true_image, test_image):
    diff = true_image.astype(float) - test_image.astype(float)
    return np.sqrt(np.mean(diff**2))


def psnr(true_image, test_image, data_range=None):
    return peak_signal_noise_ratio(true_image, test_image, data_range=data_range)


def ssim(true_image, test_image, data_range=None):
    return structural_similarity(true_image, test_image, data_range=data_range)
