import torch
import torchvision.transforms as transforms
from PIL import Image

# Example placeholder model
model = torch.load("mineral_model.pt")
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def detect_minerals(image):
    img = Image.fromarray(image)
    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(img)

    return output.tolist()
