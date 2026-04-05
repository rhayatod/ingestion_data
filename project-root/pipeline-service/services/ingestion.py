import requests
from sqlalchemy.orm import Session
from models.customer import Customer

FLASK_URL = "http://mock-server:5000/api/customers"

def fetch_all_customers():
    page = 1
    limit = 10
    all_customer = []

    while True:
        res = requests.get(FLASK_URL, params={"page": page, "limit": limit})
        data = res.json()

        customers = data["data"]

        if not customers:
            break

        all_customer.extend(customers)

        if len(customers) < limit:
            break

        page += 1

    return all_customer

def upsert_customers(db: Session, Customers):
    count = 0

    for cust in Customers:
        exist = db.get(Customer, cust["customer_id"])

        if exist:
            for key, value in cust.items():
                setattr(exist, key, value)
        else:
            upsert_customer = Customer(**cust)
            db.add(upsert_customer)

        count += 1

    db.commit()
    return count
