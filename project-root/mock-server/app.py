from flask import Flask, jsonify, request

import os
import json

app = Flask(__name__)

CUSTOMER_DATA = os.path.join(os.path.dirname(__file__), "data/customers.json")

def load_from_file():
    try:
        with open(CUSTOMER_DATA) as f:
            return json.load(f)
    except Exception:
        return []
        
@app.route("/api/health")
def health_check():
    return {"status": "OK"}

@app.route("/api/customers")
def get_customers():
    data = load_from_file()

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    start = (page - 1) * limit
    end = start + limit

    return {
        "data": data[start:end],
        "total": len(data),
        "page": page,
        "limit": limit
    }

@app.route("/api/customers/<customer_id>")
def get_customer_by_id(customer_id):
    customers = load_from_file()

    for cust in customers:
        if cust["customer_id"] == customer_id:
            return cust

    return {"error": "customer not found"}, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
