from service.utils.logger import logger
from service.configs import settings
from service.api import APIProvider
from service.server import start_server
import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    logger.info(f'Using {settings.env} config environment')
    start_server(APIProvider(title=settings.api.name,
                             openapi_url=settings.api.endpoints.prefix + settings.api.openapi_file,
                             docs_url=settings.api.endpoints.prefix + settings.api.docs_path,
                             version=settings.api.version,
                             debug=settings.debug
                             ))
