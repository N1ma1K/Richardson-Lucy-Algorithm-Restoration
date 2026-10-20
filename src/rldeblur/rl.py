import numpy as np
from scipy.signal import fftconvolve


def richardson_lucy(observed, psf, num_iteration, clip=False, record_interval=None):
    image = np.full.like(observed, fill_value=np.mean(observed))
    psf_mirror = psf[::-1, ::-1]
    history = []

    for i in range(num_iteration):
        conv = fftconvolve(image, psf, mode='same')
        conv = np.where(conv == 0, np.finfo(float).eps, conv)
        relative_blur = observed / conv
        correction = fftconvolve(relative_blur, psf_mirror, mode='same')
        image *= correction
        if clip:
            image = np.clip(image, 0, None)
        if record_interval and (i+1) % record_interval == 0:
            history.append(image.copy())
    return (image, history) if record_interval else (image, None)
