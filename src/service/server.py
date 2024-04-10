import multiprocessing
from gunicorn.app.base import BaseApplication
from service.configs import settings
from service.api import APIProvider

from service.utils.logger import StubbedGunicornLogger


class _Application(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app

        super(_Application, self).__init__()

    def init(self, parser, opts, args):
        raise NotImplementedError

    def load(self):
        return self.application

    def load_config(self):
        config = {
            key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None
        }

        for key, value in config.items():
            self.cfg.set(key.lower(), value)


def __build_options() -> dict:
    _workers = settings.api.server.workers

    if type(_workers) is str:
        if str(_workers).lower() == 'auto':
            _workers = multiprocessing.cpu_count() * 2 + 1
        else:
            _workers = 4
    else:
        _workers = int(_workers)

    return {
        "worker_class": settings.api.server.worker_class,
        "workers": _workers,
        "bind": ":%s" % settings.api.server.bind,
        "accesslog": settings.api.server.accesslog,  # pipe to stdout
        "graceful_timeout": settings.api.server.graceful_timeout,
        "timeout": settings.api.server.timeout,
        'loglevel': settings.logging.level,
        "logger_class": StubbedGunicornLogger
    }


def __build_server(app) -> _Application:
    options = __build_options()

    return _Application(app, options)


def start_server(app: APIProvider) -> None:
    server: _Application = __build_server(app.get_api())

    server.run()
