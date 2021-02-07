from typing import NewType
import json
from os import getenv
from pathlib import Path

from asgi_webdav.constants import DAVDistributeMap
from asgi_webdav.webdav import WebDAV


def parser_conf(path: str) -> dict[str, str]:
    dist_map = dict()

    try:
        with open(Path(path).joinpath('webdav.conf')) as fp:
            data = json.load(fp)
            if not isinstance(data, DAVDistributeMap) or len(data) == 0:
                raise ValueError

    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        dist_map['/'] = path

    return dist_map


WEBDAV_DATA = getenv('WEBDAV_DATA', '/data')
app = WebDAV(parser_conf(WEBDAV_DATA))

SENTRY_DSN = getenv('SENTRY_DSN', '')
if SENTRY_DSN != '':
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(dsn=SENTRY_DSN)

    app = SentryAsgiMiddleware(app)