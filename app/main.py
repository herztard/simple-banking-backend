# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.database.database import init_db, DatabaseConnection


def create_app() -> FastAPI:
    app = FastAPI(
        title="Simple Banking API",
        version="1.0.0",
        contact={
            "name": "Adilzhan Slyamgazy",
            "url": "https://github.com/herztard",
        },
        swagger_ui_parameters={
            "syntaxHighlight.theme": "monokai",
            "layout": "BaseLayout",
            "filter": True,
            "tryItOutEnabled": True,
            "onComplete": "Ok"
        },
    )

    allowed_origins = [
        "http://localhost:5173"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["X-Requested-With", "Content-Type", "Authorization", "Access-Control-Allow-Origin"],
    )

    init_db()
    print(DatabaseConnection().get_db_url())

    return app

app = create_app()

if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
