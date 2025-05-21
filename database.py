from tortoise import generate_config

import env

TORTOISE_ORM = {
    "connections": {"default": env.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

