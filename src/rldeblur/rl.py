import numpy as np
from scipy.signal import fftconvolve


def richardson_lucy(observed, psf, num_iteration, clip=False, record_interval=None):
    """    Performs Richardson-Lucy deconvolution on a 2D image.

    Parameters:
        observed (2D array): observed (blurred) image.
        psf (2D array): point-spread function (normalized to sum=1).
        num_iteration (int): number of iterations.
        clip (bool): if True, clip negative values to zero after each iter.
        record_interval (int): if given, return a list of estimates at these intervals.

    Returns:
        result (2D array): deconvolved image after num_iteration.
        history (list of 2D arrays): estimates at each record step (if record_interval set).
    """
