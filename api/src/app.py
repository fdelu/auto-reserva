from fastapi import FastAPI

from .router import router

# Can't use routePrefix in host.json due to this bug:
# https://github.com/Azure/azure-functions-python-worker/issues/1310
ROUTE_PREFIX = "/api"

app = FastAPI(
    title="Auto reservation API",
    openapi_url=f"{ROUTE_PREFIX}/openapi.json",
    docs_url=f"{ROUTE_PREFIX}/docs",
    redoc_url=f"{ROUTE_PREFIX}/redoc",
)
app.include_router(router, prefix=ROUTE_PREFIX)
