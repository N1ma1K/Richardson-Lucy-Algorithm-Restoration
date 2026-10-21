import numpy as np
import matplotlib.pyplot as plt


def asinh_stretch(image, scale=1.0):
    return np.arcsinh(image * scale)


def show_two_images(img1, img2, titles=('Original', 'Restored'), cmap='gray'):
    fig, axes = plt.subplot(1, 2, figsize=(10, 5))
    for ax, img, title in zip(axes, (img1, img2), titles):
        im = ax.imshow(img, cmap=cmap, origin='lower')
        ax.set_title(title)
        ax.axis('off')
    plt.tight_layout()
    return fig


def plot_error_vs_iteration(errors, labels=None):
    fig, ax = plt.subplots()
    n = len(errors)
    ax.plot(range(1, n+1), errors, '-o')
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Error (E.G. RMSE)")
    return fig
