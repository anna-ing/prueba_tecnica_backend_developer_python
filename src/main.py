from fastapi import FastAPI
from src.core.config import settings
from src.api.routes.cbamImport import router as cbam_router
app = FastAPI()

app=FastAPI(title=settings.PROJECT_NAME)

app.include_router(cbam_router)