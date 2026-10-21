import yaml
import numpy as np
import pandas as pd
import astropy.io as fits
import matplotlib.pyplot as plt

from rldeblur import io, psf, degrade, rl, metrics, plotting

# Expirement parameters (Can be loaded from yaml)
params = {
    'fwhm': 3.0,                 # FWHM of PSF in pixels
    'beta': 2.5,                 # Moffat beta parameter
    'peak': 1000,                # peak count after scaling
    'num_iters': 30,             # RL iterations
    'noise_seed': 12345,         # RNG seed
    'psf_mismatch_factor': 1.1,  # scale factor for wrong PSF (e.g. +10%)
}

# Load FITS
image_true, header = io.load_fits_data(
    "data/h_m51_v_s20_drz_sci.fits", cutout_size=51)

# Create PSFs
psf_true = psf.moffat_psf((51, 51), fwhm=params['fwhm'], beta=params['beta'])
psf_wrong = psf.moffat_psf(
    (51, 51), fwhm=params['fwhm'] * params["psf_mismatch_factor"], beta=params['beta'])

# Degrade image
image_blur = degrade.blur_image(image_true, psf_true)
image_blue = degrade.scale_peak(image_blur, params['peak'])
rng = np.random.default_rng(params['noise_seed'])
image_noisy = degrade.add_poisson_noise(image_blur, rng)

# Run RL
restored, history = rl.richardson_lucy(
    image_noisy, psf_wrong, params['num_iters'], record_interval=1)

# Compute metrics
err_rmse = [metrics.rmse(image_true, h) for h in history]
err_ssim = [metrics.ssim(image_true, h, data_image=image_true.max())
            for h in history]
final_rmse = metrics.rmse(image_true, restored)
final_psnr = metrics.psnr(image_true, restored, data_range=image_true.max())
final_ssim = metrics.ssim(image_true, restored, data_range=image_true.max())

# Save figures
fig1 = plotting.show_two_images(
    image_blur, restored, titles=('Blurred', 'Restored'))
fig1.savefig('results/figures/comparison.png')
fig2 = plotting.plot_error_vs_iteration(err_rmse)
fig2.savefig('results/figures/error_vs_iteration.png')

# Save metrics to CSV
df = pd.DataFrame({
    'iteration': list(range(1, len(err_rmse)+1)),
    'rmse': err_rmse,
    'ssim': err_ssim
})
df.loc[len(df)] = {'iteration': 'final',
                   'rmse': final_rmse, 'ssim': final_ssim}
df.to_csv('results/metrics.csv', index=False)
