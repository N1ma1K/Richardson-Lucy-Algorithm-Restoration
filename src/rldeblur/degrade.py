import numpy as np
from scipy.signal import fftconvolve


def blur_image(image, psf):
    return fftconvolve(image, psf, mode='same')


def scale_peak(image, peak_value):
    current_max = image.max()
    if current_max <= 0:
        raise ValueError("Image has non-positive max; cannot scale.")
    scale = peak_value / current_max
    return image * scale


def add_poisson_noise(image, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    noisy = rng.poisson(image)
    return noisy.astype(float)
