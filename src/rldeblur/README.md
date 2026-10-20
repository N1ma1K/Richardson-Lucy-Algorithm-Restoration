__init__.py
A minimal file that makes rldeblur a package, also sets a version string.

# io.py
Handles FITS I/O and cutouts. Reads a FITS file, extracts a centered cutout, subtracts background (e.g. using median), and tracks units.

# psf.py
Defines PSF models. Implements a normalized 2D Gaussian PSF and a Moffat PSF (normalized to sum to 1). The Moffat profile formula and its FWHM relation come from standard astrophysical sources.

gaussian.psf() function:
    Generates a normalized 2D Gaussian PSF of given FWHM.

    Parameters:
        shape (tuple of int): (ny, nx) array size (should be odd integers).
        fwhm (float): full width at half maximum of the Gaussian (in pixels).

    Returns:
        psf (2D numpy array): Gaussian PSF normalized to sum=1.

moffat.psf() function:
    Generates a normalized 2D Moffat PSF of given FWHM and beta parameter.
    Moffat function: I = (beta-1)/(pi*alpha^2) * [1 + (r/alpha)^2]^{-beta}
    with FWHM = 2*alpha*sqrt(2^(1/beta)-1).

    Parameters:
        shape (tuple of int): (ny, nx) PSF array size (odd integers).
        fwhm (float): desired full width at half maximum.
        beta (float): Moffat power-law index (>1).

    Returns:
        psf (2D numpy array): Moffat PSF normalized to sum=1.

# rl.py

richard_lucy() function:
    Performs Richardson-Lucy deconvolution on a 2D image.

    Parameters:
        observed (2D array): observed (blurred) image.
        psf (2D array): point-spread function (normalized to sum=1).
        num_iters (int): number of iterations.
        clip (bool): if True, clip negative values to zero after each iter.
        record_interval (int): if given, return a list of estimates at these intervals.

    Returns:
        result (2D array): deconvolved image after num_iters.
        history (list of 2D arrays): estimates at each record step (if record_interval set).
    
