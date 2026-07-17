# Database Schema Design

## Project

**Manufacturing Production Planning & Operations Automation System (MPPOAS)**

---

# Overview

The Manufacturing Production Planning & Operations Automation System is designed to automate production planning, inventory reconciliation, material requirement planning (MRP), and manufacturing operations.

The system follows a master-data-first approach where products, materials, and machines are maintained as master records, while forecasts, inventory, and production plans are transactional data.

---

# Database Design Principles

* Single source of truth
* Normalized database structure
* Rule-based planning
* Scalable architecture
* Auditable calculations
* Separation of master and transactional data

---

# Entity Overview

```
Products
│
├── Forecast
├── Inventory
├── Production Plan
└── BOM
        │
        ▼
    Materials

Machines
    │
    ▼
Production Plan
```

---

# Table 1 — Products

Purpose

Stores all manufactured products.

| Column       | Type         | Description       |
| ------------ | ------------ | ----------------- |
| product_id   | VARCHAR(20)  | Primary Key       |
| product_name | VARCHAR(100) | Product Name      |
| family       | VARCHAR(50)  | Product Family    |
| size_mm      | INTEGER      | Product Size      |
| unit         | VARCHAR(10)  | Unit of Measure   |
| status       | VARCHAR(20)  | Active / Inactive |

Example

| product_id | product_name     | family |
| ---------- | ---------------- | ------ |
| HC020      | Hose Clamp 20 mm | Small  |

---

# Table 2 — Materials

Purpose

Stores raw materials required during manufacturing.

| Column        | Type         | Description       |
| ------------- | ------------ | ----------------- |
| material_id   | VARCHAR(20)  | Primary Key       |
| material_name | VARCHAR(100) | Material Name      |
| unit          | VARCHAR(20)  | Unit of Measure   |
| status       | VARCHAR(20)  | Active / Inactive |

Example

| material_id | material_name         |
| ----------- | --------------------- |
| RM001       | Stainless Steel Strip |
| RM002       | Housing               |
| RM003       | Worm Screw            |

---

# Table 3 — Bill of Materials (BOM)

Purpose

Defines which raw materials are required to manufacture one unit of a product.

| Column            | Type           | Description                       |
| ----------------- | -------------- | --------------------------------- |
| bom_id            | SERIAL         | Primary Key                       |
| product_id        | FK → Products  | Associated Product                |
| material_id       | FK → Materials | Associated Material               |
| quantity_per_unit | DECIMAL(10,4)  | Quantity per unit of product      |
| scrap_percentage  | DECIMAL(5,2)   | Expected scrap rate (e.g. 2.50%)  |
| effective_from    | DATE           | Effective starting date           |
| effective_to      | DATE           | Effective ending date             |

Example

| Product | Material              | Quantity | Scrap% |
| ------- | --------------------- | -------- | ------ |
| HC020   | Stainless Steel Strip | 0.062 kg | 5.00%  |
| HC020   | Housing               | 1        | 0.00%  |
| HC020   | Worm Screw            | 1        | 0.00%  |

---

# Table 4 — Machines

Purpose

Stores production machine information.

| Column         | Type         | Description       |
| -------------- | ------------ | ----------------- |
| machine_id     | VARCHAR(20)  | Primary Key       |
| machine_name   | VARCHAR(100) | Machine Name      |
| line_name      | VARCHAR(50)  | Manufacturing Line|
| daily_capacity | INTEGER      | Capacity per day  |
| shift_hours    | INTEGER      | Working hours     |
| status         | VARCHAR(20)  | Active / Inactive |

Example

| Machine | Capacity       | Status |
| ------- | -------------- | ------ |
| ST01    | 3000 Units/Day | Active |
| FM01    | 2500 Units/Day | Active |

---

# Table 5 — Forecasts

Purpose

Stores monthly sales forecasts received from the Sales department.

| Column         | Type          | Description       |
| -------------- | ------------- | ----------------- |
| forecast_id    | SERIAL        | Primary Key       |
| forecast_month | DATE          | Forecast month    |
| product_id     | FK → Products | Associated Product|
| forecast_qty   | INTEGER       | Target forecast   |
| created_at     | TIMESTAMP     | Creation date     |

---

# Table 6 — Inventory

Purpose

Stores current finished product inventory information.

| Column        | Type          | Description            |
| ------------- | ------------- | ---------------------- |
| inventory_id  | SERIAL        | Primary Key            |
| product_id    | FK → Products | Associated Product (UQ)|
| opening_stock | INTEGER       | Stock at start of cycle|
| current_stock | INTEGER       | Actual on-hand stock   |
| safety_stock  | INTEGER       | Minimum safety buffer  |
| last_updated  | TIMESTAMP     | Last update timestamp  |

---

# Table 7 — Production Plans

Purpose

Stores production plans generated by the planning engine.

| Column               | Type          | Description                      |
| -------------------- | ------------- | -------------------------------- |
| plan_id              | SERIAL        | Primary Key                      |
| plan_month           | DATE          | Targeted planning month          |
| product_id           | FK → Products | Associated Product               |
| forecast_qty         | INTEGER       | Forecasted demand                |
| available_stock      | INTEGER       | Stock available at start         |
| production_required  | INTEGER       | Net production demand            |
| capacity             | INTEGER       | Total machine capacity           |
| planned_quantity     | INTEGER       | Capacity-allocated quantity      |
| pending_quantity     | INTEGER       | Over-capacity remainder          |
| capacity_utilization | DECIMAL(5,2)  | Machine capacity utilization %   |
| status               | VARCHAR(30)   | Plan Status (READY/OVER_CAPACITY)|

---

# Table 8 — Material Requirements

Purpose

Stores material requirements (MRP) derived from the production plans.

| Column               | Type           | Description                        |
| -------------------- | -------------- | ---------------------------------- |
| requirement_id       | SERIAL         | Primary Key                        |
| plan_id              | FK → Prod Plans| Reference to Production Plan       |
| product_id           | FK → Products  | Associated Product                 |
| material_id          | FK → Materials | Associated Raw Material            |
| required_quantity    | DECIMAL(12,4)  | Total requirement (includes scrap) |
| available_stock      | DECIMAL(12,4)  | Available material stock           |
| shortage_quantity    | DECIMAL(12,4)  | Stock shortage amount              |
| procurement_required | DECIMAL(12,4)  | Raw material to procure            |
| procurement_status   | VARCHAR(30)    | Procurement status (OK/REQUIRED)   |
| unit                 | VARCHAR(20)    | Unit of measure                    |
| requirement_date     | DATE           | Date requirement is needed         |
| status               | VARCHAR(30)    | MRP status                         |
| created_at           | TIMESTAMP      | Auto-generated timestamp           |
| updated_at           | TIMESTAMP      | Last modified timestamp            |

---

# Table 9 — Material Inventory

Purpose

Stores raw material inventory stock balances and safety levels.

| Column          | Type           | Description                    |
| --------------- | -------------- | ------------------------------ |
| material_id     | FK → Materials | Primary Key (Material reference)|
| available_stock | DECIMAL(12,4)  | Current available stock qty    |
| reorder_level   | DECIMAL(12,4)  | Minimum buffer trigger level   |
| location        | VARCHAR(50)    | Warehouse storage location     |
| last_updated    | TIMESTAMP      | Last update timestamp          |

---

# Table 10 — Machine Schedule

Purpose

Stores the detailed machine-level production schedule.

| Column             | Type           | Description                    |
| ------------------ | -------------- | ------------------------------ |
| schedule_id        | SERIAL         | Primary Key                    |
| plan_id            | FK → Prod Plans| Reference to Production Plan   |
| machine_id         | FK → Machines  | Allocated Machine              |
| product_id         | FK → Products  | Product to make                |
| scheduled_quantity | DECIMAL(10,2)  | Quantity assigned to machine   |
| utilization        | DECIMAL(5,2)   | Utilization % of machine capacity|
| production_date    | DATE           | Scheduled date                 |
| status             | VARCHAR(30)    | Schedule status                |
| created_at         | TIMESTAMP      | Creation timestamp             |
| updated_at         | TIMESTAMP      | Last modification timestamp    |

---

# Business Workflow

```
Sales Forecast
        │
        ▼
Forecast Validation
        │
        ▼
Inventory Check (Subtracting Safety Stock)
        │
        ▼
Capacity Check (Active Machines Only)
        │
        ▼
Material Requirement Planning (Accounting for Scrap & Material Allocation)
        │
        ▼
Machine Scheduling (Tracking Capacity Across Plans)
        │
        ▼
Production Plan & Schedule
```

---

# Core Business Rules

## Production Required

```
Production Required = max(0, Forecast Quantity − (Current Stock − Safety Stock))
```

---

## Planned Quantity

```
Planned Quantity = min(Production Required, Machine Capacity)
```

---

## Pending Quantity

```
Pending Quantity = Production Required − Planned Quantity
```

---

## Capacity Utilization

```
Capacity Utilization = (Planned Quantity / Machine Capacity) × 100
```

---

## MRP Quantity with Scrap

```
Required Qty = Planned Qty × Qty Per Unit × (1 + Scrap% / 100)
```

---

# Technology Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pandas
* Docker
* Streamlit

---

# Architecture

```
Streamlit Dashboard (Frontend)
    │
    ▼
FastAPI API (Backend REST Layer)
    │
    ▼
Business Services (Planning/MRP/Scheduling Engines)
    │
    ▼
PostgreSQL Database (via SQLAlchemy ORM)
```

---

# Version

Version: 2.0

Status: Completed
