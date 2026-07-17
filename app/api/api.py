from fastapi import APIRouter

from app.api.routes.inventory import router as inventory_router
from app.api.routes.material_requirements import router as material_requirements_router
from app.api.routes.materials import router as materials_router
from app.api.routes.mrp import router as mrp_router
from app.api.routes.planning import router as planning_router
from app.api.routes.production_plans import router as production_plans_router
from app.api.routes.products import router as products_router
from app.api.routes.schedule import router as schedule_router

api_router = APIRouter()

api_router.include_router(products_router)
api_router.include_router(materials_router)
api_router.include_router(production_plans_router)
api_router.include_router(material_requirements_router)
api_router.include_router(planning_router)
api_router.include_router(mrp_router)
api_router.include_router(schedule_router)
api_router.include_router(inventory_router)