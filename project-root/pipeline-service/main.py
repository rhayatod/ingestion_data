from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models.customer import Customer
from services.ingestion import fetch_all_customers, upsert_customers
import logging

app = FastAPI()

Base.metadata.create_all(bind=engine)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/ingest")
def ingest(db: Session = Depends(get_db)):
    logger.info("Starting ingestion process")
    try:
        data = fetch_all_customers()    
        upsert_count = upsert_customers(db, data)
        logger.info("Inserted/Updated {upsert_count} records into DB")

        return {"status": "success", "records_processed": upsert_count}
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
    raise HTTPException(status_code=500, detail="Ingestion failed")


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(Customer)

    total = query.count()
    results = query.offset((page - 1) * limit).limit(limit).all()

    if total == 0:
        logger.error("No records found in DB")

    return {
        "data": [r.__dict__ for r in results],
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer.__dict__