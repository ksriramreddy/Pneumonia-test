from fastapi import FastAPI, UploadFile ,File
from fastapi.middleware.cors import CORSMiddleware
from app.predict import predict_image
import os
import uvicorn



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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # fallback to 8000 locally
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)