import numpy as np
import pytest
from rldeblur.psf import gaussian_psf, moffat_psf


def test_gaussian_psf_properties():
    psf = gaussian_psf((51, 51), fwhm=5.0)
    assert np.isclose(psf.sum(), 1.0, rtol=1e-6)
    cy, cx = np.array(psf.shape)//2
    assert psf[cy, cx] == pytest.approx(psf.max())

    profile = psf[cy, :]
    half = profile.max()/2

    indices = np.where(profile >= half)[0]
    fwhm_est = indices[-1] - indices[0]
    assert abs(fwhm_est - 5.0) < 1.0


def test_moffat_psf_properties():
    psf = moffat_psf((51, 51), fwhm=5.0, beta=3.0)
    assert np.isclose(psf.sum(), 1.0, rtol=1e-6)
    cy, cx = np.array(psf.shape)//2
    assert psf[cy, cx] == pytest.approx(psf.max())

    profile = psf[cy, :]
    half = profile.max()/2
    indices = np.where(profile >= half)[0]
    fwhm_est = indices[-1] - indices[0]
    assert abs(fwhm_est - 5.0) < 1.0
