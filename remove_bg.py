from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import transforms
import numpy as np
import os
from u2net import U2NET  # Make sure your U-2-Net model code is imported

# Load model (make sure path exists)
model_path = "saved_models/u2net/u2net.pth"
net = U2NET(3, 1)
net.load_state_dict(torch.load(model_path, map_location='cpu'))
net.eval()

def remove_bg(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    image = Image.open(input_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
    ])
    image_tensor = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        d1, _, _, _, _, _, _ = net(image_tensor)
        pred = d1[:,0,:,:]
        pred = (pred - pred.min()) / (pred.max() - pred.min())
        pred = F.interpolate(pred.unsqueeze(0), size=image.size[::-1], mode='bilinear', align_corners=False)
        mask = pred.squeeze().numpy() * 255
    
    result = image.copy()
    result.putalpha(Image.fromarray(mask.astype(np.uint8)))
    result.save(output_path)
    print(f"Saved: {output_path}")

# Add this part to actually run it
if __name__ == "__main__":
    input_image = "test.jpg"      # replace with your input image file
    output_image = "output.png"   # replace with desired output path
    remove_bg(input_image, output_image)
