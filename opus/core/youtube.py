import os
import re
import time
import yt_dlp
import random
import asyncio
import aiohttp

from py_yt import Playlist, VideosSearch
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from typing import Union

from opus import logger
from opus.helpers import Track, utils


# ── Multi-API Config ──────────────────────────────────────────
# Keep API credentials in Render environment variables.
# ArtistBots removed because its service is suspended.
APIS = [
    {
        "name": "ShrutiBots primary",
        "url": "https://api.shrutibots.site",
        "key": os.getenv("SHRUTIBOTS_API_KEY", "").strip(),
        "param": "api_key",
        "endpoint": "/download",
    },
    {
        "name": "ShrutiBots fallback",
        "url": "https://api.shrutibots.site",
        "key": os.getenv("SHRUTIBOTS_API_KEY_FALLBACK", "").strip(),
        "param": "api_key",
        "endpoint": "/download",
    },
]

# Skip APIs without configured keys.
APIS = [api for api in APIS if api["key"]]


FAIL_THRESHOLD = 3
BLOCK_DURATION = 5 * 3600  # 5 hours
# ─────────────────────────────────────────────────────────────

DOWNLOAD_DIR = "downloads"


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="

        self.regex = re.compile(
            r"(https?://)?(www\.|m\.|music\.)?"
            r"(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)"
            r"([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+)"
        )

        self.cookies = []
        self.checked = False
        self.cookie_dir = "opus/cookies"
        self._api_index = 0
        # Reuse one keep-alive HTTP session instead of paying connection/TLS
        # setup costs for every track and API attempt.
        self._http_session = None
        # Avoid duplicate downloads when the same track is requested concurrently.
        self._download_locks = {}
        self._prefetch_tasks = set()

        # Circuit Breaker — har API ka unique identifier key se banao
        self._fail_count = {self._api_id(api): 0 for api in APIS}
        self._blocked_until = {self._api_id(api): 0 for api in APIS}

    def _api_id(self, api: dict) -> str:
        """Same URL par bhi alag key ho to unique ID banao"""
        return f"{api['url']}::{api['key']}"

    def get_cookies(self):
        if not self.checked:
            if os.path.exists(self.cookie_dir):
                for file in os.listdir(self.cookie_dir):
                    if file.endswith(".txt"):
                        self.cookies.append(f"{self.cookie_dir}/{file}")
            self.checked = True
        return random.choice(self.cookies) if self.cookies else None

    async def _get_http_session(self):
        if self._http_session is None or self._http_session.closed:
            connector = aiohttp.TCPConnector(
                limit=8, limit_per_host=4, ttl_dns_cache=300, keepalive_timeout=30
            )
            timeout = aiohttp.ClientTimeout(total=22, connect=4, sock_read=18)
            self._http_session = aiohttp.ClientSession(
                connector=connector, timeout=timeout,
                headers={"User-Agent": "OpusMusic/3.0"},
            )
        return self._http_session

    async def close(self):
        """Release pooled HTTP connections during graceful shutdown."""
        if self._http_session and not self._http_session.closed:
            await self._http_session.close()

    # ── Circuit Breaker ───────────────────────────────────────

    def _is_blocked(self, api: dict) -> bool:
        aid = self._api_id(api)
        now = time.time()

        if now < self._blocked_until[aid]:
            remaining = int((self._blocked_until[aid] - now) / 3600)
            logger.info(f"[{aid}] Blocked! ~{remaining}h remaining.")
            return True

        if self._fail_count[aid] >= FAIL_THRESHOLD:
            logger.info(f"[{aid}] Block khatam, phir se try karega.")
            self._fail_count[aid] = 0

        return False

    def _mark_fail(self, api: dict):
        aid = self._api_id(api)
        self._fail_count[aid] += 1
        logger.warning(
            f"[{api['url']}] Fail count: {self._fail_count[aid]}/{FAIL_THRESHOLD}"
        )

        if self._fail_count[aid] >= FAIL_THRESHOLD:
            self._blocked_until[aid] = time.time() + BLOCK_DURATION
            logger.warning(f"[{api['url']}] Blocked for 5 hours!")

    def _mark_success(self, api: dict):
        aid = self._api_id(api)
        self._fail_count[aid] = 0
        self._blocked_until[aid] = 0
        logger.info(f"[{api['url']}] Success! Fail count reset.")

    # ── Core Methods ──────────────────────────────────────────

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def search(self, query: str, m_id: int, video=False):
        try:
            search = VideosSearch(query, limit=1)
            results = await search.next()
        except Exception as e:
            logger.error(f"Search Error: {e}")
            return None

        if results and results.get("result"):
            data = results["result"][0]
            return Track(
                id=data.get("id"),
                channel_name=data.get("channel", {}).get("name"),
                duration=data.get("duration"),
                duration_sec=utils.to_seconds(data.get("duration")),
                message_id=m_id,
                title=data.get("title")[:25],
                thumbnail=data.get("thumbnails", [{}])[-1]["url"].split("?")[0],
                url=data.get("link"),
                view_count=data.get("viewCount", {}).get("short"),
                video=video,
            )

    async def playlist(self, limit, user, url, video):
        tracks = []
        try:
            plist = await Playlist.get(url)
            for data in plist["videos"][:limit]:
                tracks.append(
                    Track(
                        id=data.get("id"),
                        channel_name=data.get("channel", {}).get("name"),
                        duration=data.get("duration"),
                        duration_sec=utils.to_seconds(data.get("duration")),
                        title=data.get("title")[:25],
                        thumbnail=data.get("thumbnails")[-1]["url"].split("?")[0],
                        url=data.get("link").split("&list=")[0],
                        user=user,
                        view_count="",
                        video=video,
                    )
                )
        except Exception as e:
            logger.error(f"Playlist Error: {e}")
        return tracks

    async def url(self, message_1: Message):
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset: entity.offset + entity.length]
        return None

    # ── Download Methods ──────────────────────────────────────

    async def _try_single_api(self, api: dict, video_id: str, video: bool):
        try:
            youtube_url = self.base + video_id
            ext = "mp4" if video else "mp3"
            filename = f"{DOWNLOAD_DIR}/{video_id}.{ext}"
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)

            params = {
                "url": youtube_url,
                "type": "video" if video else "audio",
            }
            if api["key"] and api["param"]:
                params[api["param"]] = api["key"]

            session = await self._get_http_session()
            async with session.get(
                f"{api['url']}{api['endpoint']}",
                params=params,
            ) as resp:

                if resp.status != 200:
                    logger.warning(f"[{api['url']}] Status: {resp.status}")
                    self._mark_fail(api)
                    return None

                # Keep the larger chunk size to reduce Python/event-loop overhead.
                with open(filename, "wb") as f:
                    async for chunk in resp.content.iter_chunked(262144):
                        f.write(chunk)

            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                self._mark_success(api)
                logger.info(f"[{api['url']}] Download success ✓")
                return filename
            else:
                logger.warning(f"[{api['url']}] Empty file!")
                self._mark_fail(api)

        except Exception as e:
            logger.warning(f"[{api['url']}] Error: {e}")
            self._mark_fail(api)

        return None

    async def api_download(self, video_id: str, video: bool = False):
        available = [api for api in APIS if not self._is_blocked(api)]

        if not available:
            logger.error("Saari APIs blocked! yt-dlp fallback.")
            return None

        start = self._api_index % len(available)
        ordered = available[start:] + available[:start]
        self._api_index += 1

        for api in ordered:
            logger.info(
                f"Trying: {api['url']} key: {api['key'][:8]}... "
                f"(fails: {self._fail_count[self._api_id(api)]}/{FAIL_THRESHOLD})"
            )
            result = await self._try_single_api(api, video_id, video)
            if result:
                return result

        return None

    async def ytdlp_download(self, video_id: str, video: bool = False):
        url = self.base + video_id
        cookie = self.get_cookies()

        opts = {
            "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "nocheckcertificate": True,
            "noplaylist": True,
            "socket_timeout": 10,
            "retries": 2,
            "fragment_retries": 2,
            "concurrent_fragment_downloads": 4,
            "cachedir": False,
        }

        if cookie:
            opts["cookiefile"] = cookie

        if video:
            opts["format"] = "bestvideo+bestaudio"
        else:
            # Prefer a higher-bitrate audio-only source, but retain a fallback
            # for videos that do not expose the preferred format.
            opts["format"] = "bestaudio[abr>=128]/bestaudio"

        def run():
            with yt_dlp.YoutubeDL(opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=True)
                    return ydl.prepare_filename(info)
                except Exception as e:
                    logger.error(f"yt-dlp Error: {e}")
                    return None

        return await asyncio.to_thread(run)

    def cached_download(self, video_id: str, video: bool = False):
        """Return a completed local media file, regardless of its real extension."""
        if not video_id or not os.path.isdir(DOWNLOAD_DIR):
            return None
        for name in os.listdir(DOWNLOAD_DIR):
            if name.startswith(f"{video_id}.") and not name.endswith(
                (".part", ".ytdl", ".tmp")
            ):
                path = os.path.join(DOWNLOAD_DIR, name)
                try:
                    if os.path.isfile(path) and os.path.getsize(path) > 0:
                        return path
                except OSError:
                    continue
        return None

    async def prefetch(self, media):
        """Download a queued track in the background so the next transition is ready."""
        if not media or media.file_path or self.cached_download(media.id, media.video):
            if media and not media.file_path:
                media.file_path = self.cached_download(media.id, media.video)
            return
        try:
            media.file_path = await self.download(media.id, video=media.video)
            if media.file_path:
                logger.info(f"Prefetched queued track: {media.id}")
        except Exception as exc:
            logger.warning(f"Background prefetch failed for {media.id}: {exc}")

    async def download(self, video_id: str, video: bool = False):
        cached = self.cached_download(video_id, video)
        if cached:
            logger.info(f"Using cached media: {video_id}")
            return cached

        lock = self._download_locks.setdefault(video_id, asyncio.Lock())
        async with lock:
            cached = self.cached_download(video_id, video)
            if cached:
                return cached
            file = await self.api_download(video_id, video)
            if file and os.path.isfile(file) and os.path.getsize(file) > 0:
                return file
            logger.warning("All APIs failed/blocked, falling back to yt-dlp")
            file = await self.ytdlp_download(video_id, video)
            return file if file and os.path.isfile(file) and os.path.getsize(file) > 0 else None
