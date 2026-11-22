from fastapi import FastAPI

app = FastAPI(title="Интернет-кабинет клиента банка")

from . import models
from .clients.router import router as clients_router
from .payments.router import router as payments_router
from .products.router import router as products_router
from .support.router import router as support_router

app.include_router(clients_router)
app.include_router(products_router)
app.include_router(payments_router)
app.include_router(support_router)

@app.get("/health")
def health():
    return {
        "status": "200 OK"
    }

@app.get("/")
def hi():
    return {
        "status": "200 "
    }