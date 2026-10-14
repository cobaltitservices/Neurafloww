#!/usr/bin/env python3
"""
Image Compression and Optimization Utility.
Optimizes PNG and JPEG assets, strips redundant alpha planes from fully opaque images,
applies maximum zlib compression (level 9), and generates next-gen WebP assets.
"""

import os
import sys
import argparse
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] ImageCompressor: %(message)s")
logger = logging.getLogger("ImageCompressor")

def compress_single_image(filepath: str, webp_quality: int = 92, generate_webp: bool = True):
    """
    Compresses a single image file, optimizing PNG in-place and optionally creating WebP.
    """
    if not os.path.isfile(filepath):
        logger.error(f"File not found: {filepath}")
        return None

    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".png", ".jpg", ".jpeg", ".webp"]:
        return None

    orig_size = os.path.getsize(filepath)

    try:
        with Image.open(filepath) as im:
            mode = im.mode
            format_name = im.format

            # Check if RGBA has real transparency or is 100% opaque
            if mode == "RGBA":
                alpha = im.split()[-1]
                alpha_extrema = alpha.getextrema()
                # If minimum alpha is 255, the image is entirely opaque
                if alpha_extrema == (255, 255, 255):
                    im = im.convert("RGB")
                    mode = "RGB"

            # 1. Optimize original format in-place
            if ext == ".png":
                im.save(filepath, format="PNG", optimize=True, compress_level=9)
            elif ext in [".jpg", ".jpeg"]:
                im.save(filepath, format="JPEG", quality=webp_quality, optimize=True)

            new_size = os.path.getsize(filepath)
            png_saved = orig_size - new_size
            png_saved_pct = (png_saved / orig_size * 100) if orig_size > 0 else 0

            # 2. Generate modern WebP counterpart
            webp_size = 0
            webp_path = None
            if generate_webp and ext in [".png", ".jpg", ".jpeg"]:
                base_without_ext = os.path.splitext(filepath)[0]
                webp_path = f"{base_without_ext}.webp"
                im.save(webp_path, format="WEBP", quality=webp_quality, method=6)
                webp_size = os.path.getsize(webp_path)

            return {
                "file": filename,
                "path": filepath,
                "orig_size": orig_size,
                "new_size": new_size,
                "saved_bytes": png_saved,
                "saved_pct": png_saved_pct,
                "webp_path": webp_path,
                "webp_size": webp_size,
                "webp_saved_pct": ((orig_size - webp_size) / orig_size * 100) if orig_size > 0 else 0
            }

    except Exception as e:
        logger.error(f"Error compressing {filepath}: {e}")
        return None


def compress_directory(directory: str, webp_quality: int = 92, generate_webp: bool = True):
    """
    Compresses all images in the specified directory.
    """
    if not os.path.isdir(directory):
        logger.error(f"Directory not found: {directory}")
        return []

    results = []
    for root, _, files in os.walk(directory):
        for f in sorted(files):
            ext = os.path.splitext(f)[1].lower()
            if ext in [".png", ".jpg", ".jpeg"]:
                p = os.path.join(root, f)
                res = compress_single_image(p, webp_quality, generate_webp)
                if res:
                    results.append(res)

    return results


def print_compression_report(results):
    """
    Prints a structured tabular audit report of the compression results.
    """
    if not results:
        logger.info("No images were compressed.")
        return

    logger.info("==========================================================================================")
    logger.info("IMAGE COMPRESSION AUDIT REPORT")
    logger.info("==========================================================================================")
    header = f"{'Filename':<28} | {'Original':<10} | {'Optimized':<10} | {'Saved %':<9} | {'WebP':<10} | {'WebP Saved %':<12}"
    logger.info(header)
    logger.info("-" * len(header))

    total_orig = 0
    total_new = 0
    total_webp = 0

    for r in results:
        total_orig += r["orig_size"]
        total_new += r["new_size"]
        total_webp += r["webp_size"]
        
        orig_kb = f"{r['orig_size']/1024:.1f} KB"
        new_kb = f"{r['new_size']/1024:.1f} KB"
        saved_pct = f"-{r['saved_pct']:.1f}%"
        webp_kb = f"{r['webp_size']/1024:.1f} KB" if r['webp_size'] > 0 else "N/A"
        webp_saved_pct = f"-{r['webp_saved_pct']:.1f}%" if r['webp_size'] > 0 else "N/A"

        logger.info(f"{r['file']:<28} | {orig_kb:<10} | {new_kb:<10} | {saved_pct:<9} | {webp_kb:<10} | {webp_saved_pct:<12}")

    logger.info("-" * len(header))
    tot_orig_kb = f"{total_orig/1024:.1f} KB"
    tot_new_kb = f"{total_new/1024:.1f} KB"
    tot_saved_pct = f"-{((total_orig - total_new) / total_orig * 100):.1f}%"
    tot_webp_kb = f"{total_webp/1024:.1f} KB"
    tot_webp_saved_pct = f"-{((total_orig - total_webp) / total_orig * 100):.1f}%"

    logger.info(f"{'TOTALS':<28} | {tot_orig_kb:<10} | {tot_new_kb:<10} | {tot_saved_pct:<9} | {tot_webp_kb:<10} | {tot_webp_saved_pct:<12}")
    logger.info("==========================================================================================")
    logger.info(f"Total Disk Space Saved (In-Place PNG): {(total_orig - total_new)/1024:.1f} KB")
    logger.info(f"Total Bandwidth Saved (via WebP):     {(total_orig - total_webp)/1024:.1f} KB")
    logger.info("==========================================================================================")


def main():
    parser = argparse.ArgumentParser(description="Image Compression Utility for Web & Production Assets")
    parser.add_argument("--dir", default="dashboard/assets", help="Target directory to compress (default: dashboard/assets)")
    parser.add_argument("--file", help="Optional specific file to compress")
    parser.add_argument("--quality", type=int, default=92, help="WebP and JPEG quality setting (1-100, default: 92)")
    parser.add_argument("--no-webp", action="store_true", help="Skip generating WebP assets")

    args = parser.parse_args()

    generate_webp = not args.no_webp

    if args.file:
        res = compress_single_image(args.file, args.quality, generate_webp)
        if res:
            print_compression_report([res])
    else:
        results = compress_directory(args.dir, args.quality, generate_webp)
        print_compression_report(results)


if __name__ == "__main__":
    main()
