from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from database import  TORTOISE_ORM




@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        async with RegisterTortoise(
            app=app, config=TORTOISE_ORM, generate_schemas=True
        ):


            yield
            await Tortoise.close_connections()