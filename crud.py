from sqlalchemy.orm import Session
import models, schemas

# CREATE
def create_scan_record(db: Session, scan: schemas.ScanCreate):
    db_item = models.ScanRecord(
        filename=scan.filename,
        prediction=scan.prediction
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# READ (All)
def get_scans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ScanRecord).offset(skip).limit(limit).all()

# READ (One)
def get_scan(db: Session, scan_id: int):
    return db.query(models.ScanRecord).filter(models.ScanRecord.id == scan_id).first()

# UPDATE
def update_scan_record(db: Session, scan_id: int, scan_update: schemas.ScanUpdate):
    db_item = db.query(models.ScanRecord).filter(models.ScanRecord.id == scan_id).first()
    if db_item:
        if scan_update.status:
            db_item.status = scan_update.status
        db.commit()
        db.refresh(db_item)
    return db_item

# DELETE
def delete_scan_record(db: Session, scan_id: int):
    db_item = db.query(models.ScanRecord).filter(models.ScanRecord.id == scan_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item