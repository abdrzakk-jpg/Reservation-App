from app.services.logger import logger
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference  # UI enhancement

from app.db_connector import engine
from app.models import Base
from app.routers import CRUD

# * create models in `posts` table
Base.metadata.create_all(bind=engine)


app = FastAPI(
    docs_url=None,  # تعطيل Swagger
    redoc_url=None,  # تعطيل ReDoc
)


# * ===================|Updating-Docs-UI|=================== *#
@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="API Docs",
    )


# * ======================================================== *#


@app.get("/")  # "/" => path, .get => method
def root():
    return {"msg": "hello api !!!"}


app.include_router(CRUD.router)

# import & start scheduler
from app.services.setup_scheduler import setup_scheduler
if setup_scheduler() :
    logger.info("Scheduler Started !")
