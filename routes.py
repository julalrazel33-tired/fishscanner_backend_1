from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, crud, roboflow_utils
import shutil
import os

router = APIRouter(prefix="/scans", tags=["Fish Freshness Scans"])

@router.post("/", response_model=schemas.ScanResponse)
async def create_scan(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Save temp file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 2. Call Roboflow Workflow
        roboflow_result = roboflow_utils.run_inference(temp_path)
        
        # 3. Save to Database via CRUD
        scan_data = schemas.ScanCreate(filename=file.filename, prediction=roboflow_result)
        return crud.create_scan_record(db, scan_data)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/", response_model=list[schemas.ScanResponse])
def read_scans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_scans(db, skip=skip, limit=limit)

@router.get("/{scan_id}", response_model=schemas.ScanResponse)
def read_scan(scan_id: int, db: Session = Depends(get_db)):
    db_scan = crud.get_scan(db, scan_id)
    if not db_scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return db_scan

@router.put("/{scan_id}", response_model=schemas.ScanResponse)
def update_scan(scan_id: int, scan_update: schemas.ScanUpdate, db: Session = Depends(get_db)):
    return crud.update_scan_record(db, scan_id, scan_update)

@router.delete("/{scan_id}")
def delete_scan(scan_id: int, db: Session = Depends(get_db)):
    crud.delete_scan_record(db, scan_id)
    return {"message": "Scan deleted successfully"}