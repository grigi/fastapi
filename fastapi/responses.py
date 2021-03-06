from decimal import Decimal
from typing import Any

from starlette.responses import FileResponse  # noqa
from starlette.responses import HTMLResponse  # noqa
from starlette.responses import JSONResponse  # noqa
from starlette.responses import PlainTextResponse  # noqa
from starlette.responses import RedirectResponse  # noqa
from starlette.responses import Response  # noqa
from starlette.responses import StreamingResponse  # noqa
from starlette.responses import UJSONResponse  # noqa

try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


def _ordefault(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError  # pragma: nocoverage


class ORJSONResponse(JSONResponse):
    media_type = "application/json"
    skip_jsonable_encoder = True

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(content, default=_ordefault)
