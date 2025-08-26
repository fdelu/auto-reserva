"""
Monkey patch for Azure Functions ASGI support
https://github.com/Azure/azure-functions-python-worker/issues/1310
"""

import azure.functions as func
from azure.functions._abc import Context
from azure.functions._http_asgi import AsgiMiddleware
from azure.functions._http_wsgi import WsgiMiddleware
from azure.functions.decorators.http import HttpMethod
from azure.functions.http import HttpRequest


class AsgiFunctionApp(func.AsgiFunctionApp):
    def _add_http_app(
        self,
        http_middleware: AsgiMiddleware | WsgiMiddleware,
        function_name: str = "http_app_func",
    ) -> None:
        """Add an Asgi app integrated http function.

        :param http_middleware: :class:`WsgiMiddleware`
                                or class:`AsgiMiddleware` instance.

        :return: None
        """
        if not isinstance(http_middleware, AsgiMiddleware):
            raise TypeError("Please pass AsgiMiddleware instance as parameter.")

        asgi_middleware: AsgiMiddleware = http_middleware

        @self.function_name(name=function_name)
        @self.http_type(http_type="asgi")
        @self.route(
            methods=(method for method in HttpMethod),
            auth_level=self.auth_level,
            route="{*route}",
        )
        async def http_app_func(req: HttpRequest, context: Context):  # type: ignore
            if not self.startup_task_done:
                success = await asgi_middleware.notify_startup()
                if not success:
                    raise RuntimeError("ASGI middleware startup failed.")
                self.startup_task_done = True

            return await asgi_middleware.handle_async(req, context)
