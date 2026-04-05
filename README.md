# Data Pipeline Project (Flask + FastAPI + PostgreSQL)

## 📌 Overview

This project demonstrates a simple data pipeline using:

- **Flask** → Mock API serving customer data from JSON (Mock Server)
- **FastAPI** → Data ingestion & API service (Pipeline Service)
- **PostgreSQL** → Database storage
- **Docker Compose** → Service orchestration

### 🔄 Flow

Flask (JSON API) → FastAPI (Ingest) → PostgreSQL → FastAPI (Query API)

---

## 📁 Project Structure

```
project-root/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── database.py
    ├── models/customer.py
    ├── services/ingestion.py
    ├── Dockerfile
    └── requirements.txt
```

---

## ⚙️ Prerequisites

- Docker
- Docker Compose

---

## 🚀 How to Run

### 1. Build and start all services

```
docker-compose up --build
```

### 2. Services will run on:

- Flask Mock API → [http://localhost:5000](http://localhost:5000)
- FastAPI Service → [http://localhost:8000](http://localhost:8000)
- FastAPI Docs → [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 API Testing

### 1. Check Flask API

```
GET http://localhost:5000/api/customers
```

### 2. Ingest data into PostgreSQL

```
POST http://localhost:8000/api/ingest
```

Expected response:

```
{
  "status": "success",
  "records_processed": 20
}
```

### 3. Get customers from DB

```
GET http://localhost:8000/api/customers?page=1&limit=10
```

### 4. Get single customer

```
GET http://localhost:8000/api/customers/{id}
```

---

## 🗄️ Database Configuration

Defined in `docker-compose.yml`:

```
DATABASE_URL=postgresql://postgres:password@postgres:5432/customer_db
```

---

## 🧠 Key Features

- Load data from JSON file (not hardcoded)
- Pagination support (Flask & FastAPI)
- Data ingestion with auto-pagination
- Upsert logic (insert/update)
- PostgreSQL integration using SQLAlchemy
- Dockerized microservices setup

---

## ⚠️ Notes

- Inside Docker, use `postgres` as hostname (NOT localhost)
- Ensure at least 20 records in `customers.json`
- `created_at` is generated automatically by database

---

## 🛑 Stop Services

```
docker-compose down
```

---

---

## 👨‍💻 Author

Rahmat Hayato Darlis

This project is built as part of a backend technical test demonstrating microservices, API integration, and data pipelines.
