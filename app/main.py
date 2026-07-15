from fastapi import FastAPI

from app.api.routes import (
    products,
    materials,
    production_plans,
    material_requirements,
    planning,
    schedule,
    mrp,
    inventory,
)

app = FastAPI(
    title="Manufacturing Production Planning System API",
    description="Backend API for Production Planning and Material Requirement Planning (MRP)",
    version="1.0.0",
)

# Register Routers
app.include_router(products.router)
app.include_router(materials.router)
app.include_router(production_plans.router)
app.include_router(material_requirements.router)
app.include_router(planning.router)
app.include_router(mrp.router)
app.include_router(schedule.router)
app.include_router(inventory.router)


@app.get("/")
def root():
    return {
        "message": "Manufacturing Production Planning System API",
        "version": "1.0.0",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }