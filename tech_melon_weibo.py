import asyncio
import json
import logging
import os
from html import unescape
from xml.etree import ElementTree

import websockets
from config import setup_logging

logger = logging.getLogger(__name__)
TECH_MELON_SESSION_COOKIE = os.getenv(
    "TECH_MELON_SESSION",
    "session=.eJw1yrEOgjAQBuB3uZnl8LSFyThowszeHL1_MIRqajElxneXxfn7PhSeyIsmpEJ9ySsaMrzvEaE8ZiTqyUQ8d9zCq4qJTuon2FFalug656ih9YUcZmz7Zu_sJCwHi_4vSRfsNN7CudZ6uQ4DfX9J5CXH.ad8-tA.deMBjHjRAOBWxBkcsCErdMpXV0E",
)


def html_to_text(html: str) -> str:
    wrapped_html = f"<root>{html}</root>"
    try:
        root = ElementTree.fromstring(wrapped_html)
        text = "".join(root.itertext())
    except ElementTree.ParseError:
        text = unescape(html)
    return text.replace("\u200b", "").strip()


def extract_media_urls(media: dict) -> list[str]:
    urls: list[str] = []

    images = media.get("images")
    if isinstance(images, list):
        for image in images:
            if isinstance(image, dict):
                origin = image.get("origin")
                thumb = image.get("thumb")
                if isinstance(origin, str) and origin:
                    urls.append(origin)
                elif isinstance(thumb, str) and thumb:
                    urls.append(thumb)
            elif isinstance(image, str) and image:
                urls.append(image)

    video = media.get("video")
    if isinstance(video, dict):
        for key in ("url", "play_url", "origin", "src"):
            value = video.get(key)
            if isinstance(value, str) and value:
                urls.append(value)
                break
    elif isinstance(video, str) and video:
        urls.append(video)

    return urls


def format_weibo_event(event: dict) -> dict | None:
    if event.get("event") != "new_weibo":
        return None

    data = event.get("data")
    if not isinstance(data, dict):
        return None

    user_name = str(data.get("user") or "").strip()
    media = data.get("media") if isinstance(data.get("media"), dict) else {}

    return {
        "tweet_is_founder": False,
        "tweet_handle": user_name,
        "new_main_text": str(data.get("content") or ""),
        "retweet_sub_text": "",
        "quote_main_text": "",
        "quote_sub_text": "",
        "reply_main_text": "",
        "reply_sub_text": "",
        "sub_media_urls": [],
        "main_media_urls": extract_media_urls(media),
    }


def format_wechat_event(event: dict) -> dict | None:
    if event.get("event") != "new_wechat":
        return None

    data = event.get("data")
    if not isinstance(data, dict):
        return None

    articles = data.get("articles")
    if not isinstance(articles, list) or not articles:
        return None

    first_article = articles[0] if isinstance(articles[0], dict) else {}
    title = str(first_article.get("title") or "").strip()
    digest = str(first_article.get("digest") or "").strip()
    main_text = title
    if digest:
        main_text = f"{title}\n{digest}" if title else digest

    main_media_urls: list[str] = []
    cover = first_article.get("cover")
    if isinstance(cover, str) and cover:
        main_media_urls.append(cover)

    return {
        "tweet_is_founder": False,
        "tweet_handle": str(data.get("gzh_name") or "").strip(),
        "new_main_text": main_text,
        "retweet_sub_text": "",
        "quote_main_text": "",
        "quote_sub_text": "",
        "reply_main_text": "",
        "reply_sub_text": "",
        "sub_media_urls": [],
        "main_media_urls": main_media_urls,
    }


def parse_tech_melon_socketio_event(raw_msg: str) -> dict | None:
    if not raw_msg.startswith("42"):
        return None

    try:
        payload = json.loads(raw_msg[2:])
    except json.JSONDecodeError:
        return None

    if not isinstance(payload, list) or not payload:
        return None

    event_name = payload[0]
    if not isinstance(event_name, str):
        return None

    parsed_event = {"event": event_name}

    if len(payload) >= 2:
        parsed_event["data"] = payload[1]
        if isinstance(payload[1], dict):
            parsed_event["data"] = dict(payload[1])
            content_html = payload[1].get("content")
            if isinstance(content_html, str):
                content_text = html_to_text(content_html)
                if content_text:
                    parsed_event["data"]["content"] = content_text

    if len(payload) > 2:
        parsed_event["extra"] = payload[2:]

    return parsed_event


async def tech_melon_weibo_wss(
    session_cookie: str = TECH_MELON_SESSION_COOKIE,
) -> None:
    if not session_cookie.strip():
        raise ValueError("session_cookie 不能为空")

    cookie_header = session_cookie.strip()
    if not cookie_header.lower().startswith("session="):
        cookie_header = f"session={cookie_header}"

    async with websockets.connect(
        "wss://tech-melon.pikacyan.xyz//socket.io/?EIO=4&transport=websocket",
        origin="https://weibo.tech-melon.top",
        user_agent_header=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        ),
        additional_headers={
            "Cache-Control": "no-cache",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Pragma": "no-cache",
            "Cookie": cookie_header,
        },
        compression="deflate",
        ping_interval=None,
        ping_timeout=None,
    ) as ws:
        logger.info("Tech Melon Weibo WSS connected.")

        open_packet = await ws.recv()
        if isinstance(open_packet, bytes):
            open_packet = open_packet.decode("utf-8", "ignore")
        logger.info("socket.io open: %s", open_packet)

        if isinstance(open_packet, str) and open_packet.startswith("0"):
            await ws.send("40")
            logger.info("socket.io namespace connected.")

        async for message in ws:
            if isinstance(message, bytes):
                message = message.decode("utf-8", "ignore")

            if message == "2":
                await ws.send("3")
                continue

            parsed_event = parse_tech_melon_socketio_event(message)
            if parsed_event:
                if parsed_event.get("event") == "server_status":
                    continue
                if parsed_event.get("event") not in {"new_weibo", "new_wechat"}:
                    continue
                if parsed_event.get("event") == "new_weibo":
                    formatted_weibo = format_weibo_event(parsed_event)
                    if formatted_weibo:
                        logger.info(
                            "tech-melon weibo:\n%s",
                            json.dumps(formatted_weibo, ensure_ascii=False, indent=2),
                        )
                        continue
                if parsed_event.get("event") == "new_wechat":
                    formatted_wechat = format_wechat_event(parsed_event)
                    if formatted_wechat:
                        logger.info(
                            "tech-melon wechat:\n%s",
                            json.dumps(formatted_wechat, ensure_ascii=False, indent=2),
                        )
                        continue
                continue


if __name__ == "__main__":
    setup_logging()
    asyncio.run(tech_melon_weibo_wss())
