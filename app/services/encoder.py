from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import torch
import numpy as np

# Load the DINOv2 model once at module level
dino_processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base")
dino_model = AutoModel.from_pretrained("facebook/dinov2-base")

def image_to_vector(image_array: np.ndarray) -> list:
    """
    Encodes an image into a feature vector using DINOv2.
    """
    # image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = Image.fromarray(image_array.astype(np.uint8))
    inputs = dino_processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = dino_model(**inputs)
        pooled = outputs.last_hidden_state.mean(dim=1)  # Mean pool over tokens

    return pooled[0].tolist()
