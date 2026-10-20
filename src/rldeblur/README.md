Includes file and function descriptions.

# __init__.py
    A minimal file that makes rldeblur a package, also sets a version string.

# io.py
    Handles FITS I/O and cutouts. Reads a FITS file, extracts a centered cutout, subtracts background (e.g. using median), and tracks units.

    load_fits_data() function:
    Parameters:
        filename (str): Path to FITS file.
        cutout_size (int): Size (pixels) of square cutout. If None, use full image.
        target_pos (tuple of int): (x, y) center for cutout; default centers in image.

    Returns:
        image (2D numpy array): background-subtracted image.
        header (fits.Header): the FITS header.

# psf.py
    Defines PSF models. Implements a normalized 2D Gaussian PSF and a Moffat PSF (normalized to sum to 1). The Moffat profile formula and its FWHM relation come from standard astrophysical sources.

    gaussian.psf() function:
        Generates a normalized 2D Gaussian PSF of the given FWHM.

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
    
# degrade.py
    Simulates a blurred and noisy observation from a "true" image. It contains functions to convolve with a PSF, scale peak brightness, and add Poisson noise.

    blur_image() function:
    Convolve image with PSF using FFT for efficiency.

    scale_peak() function:
    Scales image so that its maximum equals peak_value.

    add_poisson_noise() function:
    Adds Poisson noise to an image. 
    The input image is treated as expected counts, noise ~ Poisson(counts). 
    rng: numpy.random.Generator for reproducibility.


# plotting.py
    Contains helper functions for consistent image display and plotting. For example, we might implement asinh scaling for astronomical image contrast and routines to plot side-by-side comparisons and error curves.

    asinh_stetch() function:
    Applies an asinh stretch before display.

    show_two_images() function:
    Display two images side-by-side for comparison

    plot_error_vs_iteration() function:
    Plot error (or metric) vs iteration number.
    errors: sequence of error values.
    labels: optional list of metric names corresponding to each error series.


# metrics.py
    Defines image quality metrics: RMSE, PNSR, SSIM. 

    rmse() function:
    Root-Mean-Square error between two iamges.

    psnr() function
    Peak Signal-to-Noise Ratio (in dD). Uses skimage implementation when available.

    ssim() function:
    Structural Similarity Index (1 means identical). Uses skimage implementation. 
