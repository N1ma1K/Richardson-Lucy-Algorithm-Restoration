# Automates downloading FITS files from URLs, skippina already existing files and recording provinence in a JSON manifest.

# download_file() function:
#    Download file from URL to outdir. Skip if exists.
#    Record metadata (target, filter, etc) by reading FITS header.

import argparse
import json
import os
import requests
from astropy.io import fits
from datetime import datetime


def download_file(url, outdir='data'):
    os.makedirs(outdir, exist_ok=True)
    filename = os.path.basename(url)
    outpath = os.path.join(outdir, filename)
    if os.path.exists(outpath):
        print(f"Skipping existing file {filename}")
    else:
        print(f"Downloading {url}...")
        r = requests.get(url)
        r.raise_for_status()
        with open(outpath, "wb") as f:
            f.write(r.content)
    with fits.open(outpath) as hdul:
        header = hdul[0].header
    entry = {
        "filename": filename,
        "url": url,
        "download_date": datetime.utcnow().isoformat(),
        "target": header.get("OBJECT", ""),
        "filter": header.get("FILTER", ""),
        "BUNIT": header.get("BUNIT", ""),
        "EXPTIME": header.get("EXPTIME", ""),
        "PIXSCALE": header.get("PIXSCALE", ""),
    }
    return entry


def main(urls, outdir='data', manifest_file='data/manifest.json'):
    manifest = []
    for url in urls:
        entry = download_file(url, outdir)
        manifest.append(entry)

    with open(manifest_file, 'w') as mf:
        json.dump(manifest, mf, indent=2)
        print(f"Wrote manifest to {manifest_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', nargs='+',
                        help='URLs of FITS files to download')
    args = parser.parse_args()
    main(args.urls)
