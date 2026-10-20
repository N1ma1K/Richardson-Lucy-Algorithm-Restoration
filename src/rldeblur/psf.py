import numpy as np


def gaussian_psf(shape, fwhm):
    """
    Generate a normalized 2D Gaussian PSF of given FWHM.

    Parameters:
        shape (tuple of int): (ny, nx) array size (should be odd integers).
        fwhm (float): full width at half maximum of the Gaussian (in pixels).

    Returns:
        psf (2D numpy array): Gaussian PSF normalized to sum=1.
    """
    y, x = np.indices(shape)
    cy, cx = (shape[0]//2, shape[1]//2)
    sigma = fwhm / (2*np.sqrt(2*np.log(2)))
    psf = np.exp(-0.5 * (((x-cx)**2 + (y-cy)**2) / sigma**2))
    psf /= psf.sum()
    return psf


def moffat_psf(shape, fwhm, beta=2.5):
    """
    Generate a normalized 2D Moffat PSF of given FWHM and beta parameter.
    Moffat function: I = (beta-1)/(pi*alpha^2) * [1 + (r/alpha)^2]^{-beta}
    with FWHM = 2*alpha*sqrt(2^(1/beta)-1).

    Parameters:
        shape (tuple of int): (ny, nx) PSF array size (odd integers).
        fwhm (float): desired full width at half maximum.
        beta (float): Moffat power-law index (>1).

    Returns:
        psf (2D numpy array): Moffat PSF normalized to sum=1.
    """
    if beta <= 1:
        raise ValueError("beta must be > 1 for a valid Moffat PSF")
    y, x = np.indices(shape)
    cy, cx = (shape[0]//2, shape[1]//2)
    alpha = fwhm / (2 * np.sqrt(2**(1/beta) - 1))
    rr_sq = ((x - cx)**2 + (y - cy)**2) / alpha**2
    psf = (beta - 1) / (np.pi * alpha**2) * (1 + rr_sq) ** (-beta)
    psf /= psf.sum()
    return psf
