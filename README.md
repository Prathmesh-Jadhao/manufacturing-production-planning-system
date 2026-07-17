# Manufacturing Production Planning System

A full-stack **Production Planning & Material Requirement Planning (MRP)** system for manufacturing operations.

## Features

- **Production Planning Engine** — Converts sales forecasts into capacity-constrained production plans
- **MRP Engine** — BOM explosion to derive raw material requirements with scrap factor accounting
- **Machine Scheduling** — Allocates production across machines respecting capacity limits
- **Inventory Management** — Tracks product and material stock levels against safety thresholds
- **Interactive Dashboard** — Streamlit-based UI with charts, KPIs, and detailed data tables
- **REST API** — FastAPI backend with documented endpoints (Swagger UI at `/docs`)

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend API | FastAPI (Python) |
| Database | PostgreSQL 17 |
| ORM | SQLAlchemy 2.0 |
| Dashboard | Streamlit |
| Data Validation | Pydantic v2 |
| Infrastructure | Docker Compose |

## Architecture

```
Streamlit Dashboard  →  FastAPI REST API  →  PostgreSQL
     (Port 8501)          (Port 8000)         (Port 5432)
```

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose

### 1. Start the Database
Ensure your PostgreSQL database is running. If using Docker, you can run:
```bash
docker-compose up -d
```

### 2. Activate Virtual Environment & Install Dependencies
Activate the project's virtual environment:
```powershell
# Windows PowerShell
.\venv\Scripts\activate
```
Install dependencies (if not already installed):
```bash
pip install -r requirements.txt
```

### 3. Recreate Tables & Seed Data
To apply the correct schema constraints and load the sample data:
```bash
python scripts/recreate_db.py
```

### 4. Start the API Server
Start the Uvicorn server using the virtual environment's python:
```bash
python -m uvicorn app.main:app --reload
```
API documentation is available at: http://127.0.0.1:8000/docs

### 5. Start the Dashboard
In a new terminal window (with the virtual environment activated), start Streamlit:
```bash
streamlit run dashboard/app.py
```
Dashboard available at: http://localhost:8501

## Project Structure

```
├── app/
│   ├── api/routes/         # API endpoint handlers
│   ├── core/               # Config, database, logging
│   ├── models/             # SQLAlchemy ORM models
│   ├── schemas/            # Pydantic response schemas
│   └── services/           # Business logic engines
├── dashboard/
│   ├── app.py              # Main Streamlit dashboard
│   ├── helpers.py          # Shared API helpers
│   └── pages/              # Dashboard sub-pages
├── data/raw/               # CSV seed data files
├── docs/                   # Project documentation
├── scripts/                # CLI utilities
├── docker-compose.yml      # PostgreSQL container
└── requirements.txt        # Python dependencies
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List all products |
| GET | `/materials/` | List all materials |
| GET | `/production-plans/` | List production plans |
| GET | `/material-requirements/` | List material requirements |
| GET | `/inventory/product` | Product inventory levels |
| GET | `/inventory/material` | Material inventory levels |
| GET | `/schedule/` | Machine schedules |
| POST | `/planning/run` | Trigger production planning |
| POST | `/mrp/run` | Trigger MRP calculation |
| POST | `/schedule/run` | Trigger machine scheduling |
| GET | `/health` | Health check |

All GET endpoints support `skip` and `limit` query parameters for pagination.

## Business Logic

### Planning Engine
```
Production Required = Forecast Qty − (Current Stock − Safety Stock)
Planned Quantity = min(Production Required, Remaining Capacity)
```

### MRP Engine
```
Required Qty = Planned Qty × Qty Per Unit × (1 + Scrap% / 100)
Shortage = max(0, Required Qty − Usable Stock − Already Allocated)
```

### Machine Scheduler
```
Allocation = min(Remaining Plan Qty, Available Machine Capacity)
Utilization = (Allocation / Monthly Machine Capacity) × 100
```
