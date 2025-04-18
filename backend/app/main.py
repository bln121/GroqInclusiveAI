from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers
from app.api.routes import translationRoutes, speechRoutes, chatRoutes
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Inclusive AI application",
    version="1.0.0"
)

# CORS setup (uses values from .env via config)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(translationRoutes.router, prefix=settings.API_V1_STR, tags=["translation"])
app.include_router(chatRoutes.router, prefix=settings.API_V1_STR, tags=["chat"])
app.include_router(speechRoutes.router, prefix=settings.API_V1_STR, tags=["speech"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)