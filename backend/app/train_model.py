import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import torch.optim as optim
from torchvision import transforms , models
from PIL import Image
from tqdm import tqdm
from sklearn.metrics import accuracy_score
print("libraries imported ")
class PneumoniaData(Dataset):
    def __init__(self,root_dir,transform=None,):
        super().__init__()
        self.root_dir = root_dir    
        self.transform = transform
        self.image_paths = []
        self.lables = []
        for label in ["NORMAL","PNEUMONIA"]:
            clss_dir = os.path.join(root_dir , label)
            for image_name in os.listdir(clss_dir):
                self.image_paths.append(os.path.join(clss_dir,image_name))
                self.lables.append(0 if label == "NORMAL" else 1)
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, index):
        image_path = self.image_paths[index]
        image  = Image.open(image_path).convert("RGB")
        label = self.lables[index]

        if self.transform:
            image = self.transform(image)

        return image , label
    
print("class defined")
    
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485 , 0.456 , 0.406],std=[0.229 , 0.224 , 0.225])
])

train_dataset = PneumoniaData(root_dir="chest_xray/train" , transform=transform)
test_dataset = PneumoniaData(root_dir="chest_xray/test" , transform=transform)
val_dataset = PneumoniaData(root_dir="chest_xray/val" , transform=transform)

print("datasets loaded")
train_loader = DataLoader(train_dataset , batch_size=32 , shuffle=True)
test_loader = DataLoader(test_dataset , batch_size=32 , shuffle=False)
val_loader = DataLoader(val_dataset , batch_size=32 , shuffle=False)
print("dataloaders created")

model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 2)  # Adjusting the final layer for binary classification
# print(train_dataset[5215][1])

loss_fn = nn.CrossEntropyLoss() # this is a loss function 
optimizer = optim.SGD(model.parameters(),lr=0.003) # optimizer, used to update the model weights buy lowering it to the idel value, it used gradient descent algorithm
Epochs = 4

print(model.state_dict())
# for epoch in tqdm(range(Epochs)):
#     model.train()
#     train_loss = 0.0
#     for images , lab in tqdm(train_loader):
#         y_pred = model(images)
#         loss = loss_fn(y_pred,lab) 
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()

#         train_loss += loss
#     print(f"""
#     Epoch {epoch+1}/{Epochs} : {train_loss/len(train_loader)}
# """)
# print(model.state_dict())
# torch.save(model.state_dict(),"pneumonia_model.pth")
#     model.eval()

model.load_state_dict(torch.load("pneumonia_model.pth"))
print(model.state_dict())



