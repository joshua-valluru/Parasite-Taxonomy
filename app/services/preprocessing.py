import cv2
import numpy as np
from albumentations import Compose, HorizontalFlip, VerticalFlip, RandomRotate90, HueSaturationValue

def normalize_image(img):
    return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

def apply_augmentations(img):
    augment = Compose([
        HorizontalFlip(p=0.5),
        VerticalFlip(p=0.5),
        RandomRotate90(p=0.5),
        HueSaturationValue(p=0.5)
    ])
    augmented = augment(image=img)
    return augmented["image"]

def crop_roi(img):
    # Very naive center crop — replace with mask-based or Hough circle logic if needed
    h, w = img.shape[:2]
    margin = int(min(h, w) * 0.1)
    return img[margin:h-margin, margin:w-margin]

def preprocess_image(image_bytes):
    # Load image from bytes
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Normalize color brightness
    img = normalize_image(img)

    # Uncomment once etermined good ROI crop for provided samples
    # img = crop_roi(img)

    # Currently do not need to apply augmentations, since purely focused on feature extraction and retrieval 
    # img = apply_augmentations(img)

    return img
