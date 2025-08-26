import azure.functions as func
from src.asgi_function_app import AsgiFunctionApp
from src.app import app as inner_app

app = AsgiFunctionApp(app=inner_app, http_auth_level=func.AuthLevel.ANONYMOUS)
