from enum import verify
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, book, search, research, profile

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
