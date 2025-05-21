from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from tortoise.contrib.fastapi import tortoise_exception_handlers
import env
import hook
from routers import (
    auth_router,
    dispatch_router
)

app = FastAPI(
    title="Swift API",
    lifespan=hook.lifespan,
    exception_handlers=tortoise_exception_handlers(),
    default_response_class=responses.ORJSONResponse,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=env.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)
app.include_router(auth_router.router)
app.include_router(dispatch_router.router)
