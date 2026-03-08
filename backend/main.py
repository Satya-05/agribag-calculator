from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from database import init_db, save_record, get_all_records, get_farmer_records, delete_record
from image_processor import process_page

# Initialize FastAPI app
app = FastAPI(title="AgriBag Calculator API")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize database when server starts
init_db()

# Uploads folder path
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "AgriBag Calculator API is running!"}

@app.post("/process-image")
async def process_image(
    file: UploadFile = File(...),
    farmer_name: str = Form(...),
    date: str = Form(...)
):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        print(f"Image saved: {file_path}")

        result = process_page(file_path)

        if result["success"]:
            result["farmer_name"] = farmer_name
            result["date"] = date
            print(f"Image processed for farmer: {farmer_name}")

        os.remove(file_path)

        return result

    except Exception as e:
        print(f"Error: {e}")
        return {
            "success": False,
            "error": str(e),
            "grid": [],
            "column_sums": [0, 0, 0, 0],
            "total": 0
        }

@app.post("/save-record")
async def save_record_endpoint(request: Request):
    try:
        data = await request.json()
        save_record(
            farmer_name=data['farmer_name'],
            date=data['date'],
            total_weight=data['total_weight'],
            column_sums=data['column_sums']
        )
        return {"success": True}

    except Exception as e:
        print(f"Error saving record: {e}")
        return {"success": False, "error": str(e)}

@app.delete("/records/{record_id}")
async def delete_record_endpoint(record_id: int):
    try:
        delete_record(record_id)
        return {"success": True}

    except Exception as e:
        print(f"Error deleting record: {e}")
        return {"success": False, "error": str(e)}

@app.get("/records")
def get_records():
    try:
        records = get_all_records()
        result = []
        for r in records:
            result.append({
                "id": r[0],
                "farmer_name": r[1],
                "date": r[2],
                "total_weight": r[3],
                "col1_sum": r[4],
                "col2_sum": r[5],
                "col3_sum": r[6],
                "col4_sum": r[7],
                "created_at": r[8]
            })
        return {"success": True, "records": result}

    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/records/{farmer_name}")
def get_farmer(farmer_name: str):
    try:
        records = get_farmer_records(farmer_name)
        result = []
        for r in records:
            result.append({
                "id": r[0],
                "farmer_name": r[1],
                "date": r[2],
                "total_weight": r[3],
                "col1_sum": r[4],
                "col2_sum": r[5],
                "col3_sum": r[6],
                "col4_sum": r[7],
                "created_at": r[8]
            })
        return {"success": True, "records": result}

    except Exception as e:
        return {"success": False, "error": str(e)}