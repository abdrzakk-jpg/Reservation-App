from app.routers import SMS
from starlette.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db_connector import engine
from app.models import Base
from app.routers import CRUD

# * create models in `posts` table
Base.metadata.create_all(bind=engine)


app = FastAPI(
    docs_url=None,  # تعطيل Swagger
    redoc_url=None,  # تعطيل ReDoc
)

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"], # ["*"] just in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# from scalar_fastapi import get_scalar_api_reference  # UI enhancement
# # * ===================|Updating-Docs-UI|=================== *#
# @app.get("/docs", include_in_schema=False)
# async def scalar_docs():
#     return get_scalar_api_reference(
#         openapi_url=app.openapi_url,
#         title="API Docs",
#     )


# # * ======================================================== *#



FRONTEND_DIR = Path(__file__).parent / "static" / "frontend"
app.mount(
    "/assets",
    StaticFiles(directory=FRONTEND_DIR / "assets"),
    name="assets",
)

# serve the frontend (static folder)
@app.get("/")  # return the index.html content instead RAW Json
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")






# import & start scheduler
from app.services.setup_scheduler import setup_scheduler
setup_scheduler()

app.include_router(CRUD.router) # add crud routes
app.include_router(SMS.router) # add SMS-check endpoint