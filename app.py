import asyncio
import logging
import os

import websockets
from config import setup_logging
from websockets import ClientConnection, ServerConnection

logger = logging.getLogger(__name__)

UPSTREAM_URL = "wss://weibo.tech-melon.top/socket.io/?EIO=4&transport=websocket"
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 8765
TECH_MELON_SESSION_COOKIE = os.getenv(
    "TECH_MELON_SESSION",
    "session=.eJw1yrEOgjAQBuB3uZnl8LSFyThowszeHL1_MIRqajElxneXxfn7PhSeyIsmpEJ9ySsaMrzvEaE8ZiTqyUQ8d9zCq4qJTuon2FFalug656ih9YUcZmz7Zu_sJCwHi_4vSRfsNN7CudZ6uQ4DfX9J5CXH.ad8-tA.deMBjHjRAOBWxBkcsCErdMpXV0E",
)


def build_cookie_header(session_cookie: str) -> str:
    cookie_header = session_cookie.strip()
    if not cookie_header:
        raise ValueError("session_cookie 不能为空")
    if not cookie_header.lower().startswith("session="):
        cookie_header = f"session={cookie_header}"
    return cookie_header


async def relay_messages(
    source: ClientConnection | ServerConnection,
    target: ClientConnection | ServerConnection,
) -> None:
    async for message in source:
        await target.send(message)


async def handle_client(client_ws: ServerConnection) -> None:
    session_cookie = build_cookie_header(TECH_MELON_SESSION_COOKIE)

    logger.info("客户端已连接，开始建立上游连接")
    async with websockets.connect(
        UPSTREAM_URL,
        origin="https://weibo.tech-melon.top",
        user_agent_header=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        ),
        additional_headers={
            "Cache-Control": "no-cache",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Pragma": "no-cache",
            "Cookie": session_cookie,
        },
        compression="deflate",
        ping_interval=None,
        ping_timeout=None,
    ) as upstream_ws:
        logger.info("上游连接成功，开始双向转发")
        client_to_upstream = asyncio.create_task(relay_messages(client_ws, upstream_ws))
        upstream_to_client = asyncio.create_task(relay_messages(upstream_ws, client_ws))

        done, pending = await asyncio.wait(
            {client_to_upstream, upstream_to_client},
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        await asyncio.gather(*pending, return_exceptions=True)

        for task in done:
            exc = task.exception()
            if exc is not None:
                raise exc


async def main() -> None:
    async with websockets.serve(handle_client, LISTEN_HOST, LISTEN_PORT):
        logger.info("WSS 中转已启动: ws://%s:%s", LISTEN_HOST, LISTEN_PORT)
        await asyncio.Future()


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
