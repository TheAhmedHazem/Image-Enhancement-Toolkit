import io
from PIL import Image

def pil_to_bytes(img):
    """Convert a PIL Image to bytes."""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def bytes_to_pil(img_bytes):
    """Convert bytes back to a PIL Image."""
    return Image.open(io.BytesIO(img_bytes))
