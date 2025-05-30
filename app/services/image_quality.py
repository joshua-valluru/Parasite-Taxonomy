import cv2
import numpy as np
from PIL import Image
import io

def get_relative_patch(image, fraction=0.1):
    """
    Extracts a square patch from the top-left corner of the image,
    with each side equal to `fraction` of the image width/height.
    """
    h, w = image.shape[:2]
    patch_h = int(h * fraction)
    patch_w = int(w * fraction)
    
    # Make sure patch is at least 1 pixel
    patch_h = max(patch_h, 1)
    patch_w = max(patch_w, 1)
    
    return image[0:patch_h, 0:patch_w]

def assess_image_quality(image_bytes: bytes) -> dict:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    np_img = np.array(img)
    gray_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)

    # 1. Sharpness (Laplacian variance)
    sharpness = cv2.Laplacian(gray_img, cv2.CV_64F).var()

    # 2. Histogram clipping
    hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
    black_clip = hist[0][0]
    white_clip = hist[-1][0]

    # 3. Background std deviation
    # Obtain a background patch size relative to the input image
    bg_patch = get_relative_patch(gray_img)
    bg_std = np.std(bg_patch)

    return {
        "sharpness": sharpness,
        "black_clip": float(black_clip),
        "white_clip": float(white_clip),
        "bg_std": bg_std
    }
