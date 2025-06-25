from fastapi import FastAPI, UploadFile ,File
from fastapi.middleware.cors import CORSMiddleware
from app.predict import predict_image



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def goto():
    return {"message" : "server started, go to /predict"}

@app.post("/predict")
async def predict(file : UploadFile = File(...)):
    if not file:
        return {"message" : "No image found to predict"}
    try:
        image = await file.read()
        predicted = predict_image(image)
        return predicted
    except Exception as e:
        print(e)
