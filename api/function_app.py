import azure.functions as func

from src.app import app as inner_app

app = func.AsgiFunctionApp(app=inner_app, http_auth_level=func.AuthLevel.ANONYMOUS)
