from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service.routers import asr
from service.configs import settings
from service.utils.logger import logger


class APIProvider:

    def __init__(self,
                 title: Optional[str] = 'API',
                 openapi_url: Optional[str] = '/openapi.json',
                 version: Optional[str] = "0.0.1",
                 docs_url: Optional[str] = "/docs",
                 debug: bool = False
                 ) -> None:
        self.api = FastAPI(title=title, openapi_url=openapi_url, docs_url=docs_url,
                           version=version, debug=debug)
        self.configure_middlewares()
        self.configure_routes()
        self.logger = logger.bind(classname=self.__class__.__name__)
        self.logger.debug('API configured')

    def configure_middlewares(self):
        self.api.add_middleware(CORSMiddleware,
                                **settings.api.cors)

    def configure_routes(self):
        self.api.include_router(asr.router)

    def get_api(self) -> FastAPI:
        return self.api
