import os
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms ,models
from io import BytesIO
import tracemalloc
tracemalloc.start()

model = models.resnet18(weights = None) #Resnet18 is an CNN architecture a varient or Residual network with 18 layers. It can train very deep neural network without having vanishing gradient probelm by using skip connection.
model.fc = nn.Linear(model.fc.in_features,2) # this is the last layer we are adding to resnet. It final fully connected layer (dense) layer just like how we add for CNNs, and the 2 represents the output classes we are expecting , "NORMAL" and "PNEUMONIA"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "pneumonia_model.pth")
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

model.eval()
def predict_image(image_path):
    try:
        # image = Image.open(image_path).convert("RGB")
        image = Image.open(BytesIO(image_path)).convert("RGB")
        image = transform(image).unsqueeze(0)
        # print(image.shape)
        with torch.no_grad():
            output = model(image)
            predicted = torch.argmax(output,1).item()
            # print(output)
            print(predicted)
        return {"predicted": predicted}
    except Exception as e:
        return {"message" : str(e)}
    
# predict_image("backend/chest_xray/train/PNEUMONIA/person1_bacteria_1.jpeg")
# predict_image("backend/chest_xray/train/NORMAL/IM-0119-0001.jpeg")
# predict_image("backend/chest_xray/train/PNEUMONIA/person7_bacteria_28.jpeg")
# predict_image("backend/chest_xray/train/NORMAL/IM-0141-0001.jpeg")
# predict_image("backend/chest_xray/train/NORMAL/IM-0142-0001.jpeg")
# predict_image("backend/chest_xray/train/NORMAL/IM-0143-0001.jpeg")
