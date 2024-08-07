import json
from typing import Dict

from starlette.responses import JSONResponse, PlainTextResponse
import logging


class ResponseError(Exception):
    def __init__(self, status_code=500, fields: Dict = {}):
        self.status_code = status_code
        for key in fields:
            setattr(self, key, fields[key])

    def __repr__(self):
        logging.error(self.__dict__)
        return PlainTextResponse(str(self.__dict__), status_code=self.status_code)


def response(data, skip=0, limit=100):
    if isinstance(data, ResponseError):
        return data.__repr__()
    else:
        payload = {
            'status': "success",
            'meta': {
                'count': len(data),
                'skip': skip,
                'limit': limit,
            },
            'link': "",
            'data': data[skip:skip + limit] if isinstance(data, list) or len(data) > 1 or len(data) == 0
            else data[skip:skip + limit]
        }
    return payload


def request():
    ...
