import json
import asyncio

from mitmproxy import http


def format_response(data):
    return http.Response.make(
        200, json.dumps(data), {'content-type': 'application/json;charset=utf-8'}
    )


def async_to_sync(awaitable):
    return asyncio.get_event_loop().run_until_complete(
        asyncio.to_thread(awaitable))
