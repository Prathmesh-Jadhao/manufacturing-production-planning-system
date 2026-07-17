import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import (
    inventory,
    material_requirements,
    materials,
    mrp,
    planning,
    production_plans,
    products,
    schedule,
)
from app.core.config import settings
from app.core.logging import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Manufacturing Production Planning System API",
    description="Backend API for Production Planning and Material Requirement Planning (MRP)",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
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
        "status": "Running",
    }


@app.get("/health")
def health():
    return {"status": "Healthy"}