import os
import gdown

# Directory where the model will be stored
MODEL_DIR = "model"
os.makedirs(MODEL_DIR, exist_ok=True)

# Google Drive file ID extracted from your shared link
file_id = "1OKSoY08kkPukfiQwNoKNoUf_I8ioPCDP"
output_path = os.path.join(MODEL_DIR, "u2net.pth")

# Check if the model file already exists
if not os.path.exists(output_path):
    print("Downloading model file...")
    # Construct the direct download URL
    url = f"https://drive.google.com/uc?id={file_id}"
    # Download the file
    gdown.download(url, output_path, quiet=False)
else:
    print("Model file already exists.")
