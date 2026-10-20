import numpy as np


def gaussian_psf(shape, fwhm):
    y, x = np.indices(shape)
    cy, cx = (shape[0]//2, shape[1]//2)
    sigma = fwhm / (2*np.sqrt(2*np.log(2)))
    psf = np.exp(-0.5 * (((x-cx)**2 + (y-cy)**2) / sigma**2))
    psf /= psf.sum()
    return psf


def moffat_psf(shape, fwhm, beta=2.5):
    if beta <= 1:
        raise ValueError("beta must be > 1 for a valid Moffat PSF")
    y, x = np.indices(shape)
    cy, cx = (shape[0]//2, shape[1]//2)
    alpha = fwhm / (2 * np.sqrt(2**(1/beta) - 1))
    rr_sq = ((x - cx)**2 + (y - cy)**2) / alpha**2
    psf = (beta - 1) / (np.pi * alpha**2) * (1 + rr_sq) ** (-beta)
    psf /= psf.sum()
    return psf
