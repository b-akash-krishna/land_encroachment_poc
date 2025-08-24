import uvicorn
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os
import shutil
import json
import cv2
import time
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Import the Celery app and task
from src.tasks import process_image_for_encroachment

app = FastAPI()

# Configuration
TEMP_UPLOAD_DIR = "temp_uploads"
SECRET_KEY = "your-secret-key"  # Change this in production
ALGORITHM = "HS256"

# A fake user for demonstration purposes
FAKE_USER = {
    "username": "admin",
    "password": "password"
}

# JWT-related functions
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # In a real app, you would fetch the user from a database
        if username != FAKE_USER["username"]:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

# Configure CORS
origins = ["*"]  # Allows all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect root URL to docs
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.on_event("startup")
async def startup_event():
    os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

# Login endpoint to get a JWT token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != FAKE_USER["username"] or form_data.password != FAKE_USER["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": FAKE_USER["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoint
@app.get("/protected-data")
async def get_protected_data(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, you are authenticated."}

@app.post("/analyze_image/")
async def analyze_image(file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    """
    API endpoint that queues an image for background processing.
    """
    try:
        file_path = os.path.join(TEMP_UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        dummy_telemetry = {
            "location": (-74.006, 40.7128),
            "altitude": 100, # meters
            "orientation": 0 # degrees
        }
        
        task = process_image_for_encroachment.delay(file_path, dummy_telemetry)
        
        return {"status": "processing", "message": "Image queued for analysis.", "task_id": task.id}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/generate_report/")
async def create_report(encroachments_json: str):
    """
    Generates a PDF report from a JSON string of encroachment data.
    """
    try:
        encroachments = json.loads(encroachments_json)
        report_path = generate_pdf_report(encroachments, output_path=f"reports/encroachment_report.pdf")
        
        return {"report_url": "http://localhost:8000/reports/encroachment_report.pdf"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("src.backend.main:app", host="0.0.0.0", port=8000, reload=True)