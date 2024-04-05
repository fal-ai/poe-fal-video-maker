from __future__ import annotations

from typing import AsyncIterable

import os
import fal_client
import fastapi_poe as fp
import httpx
from dataclasses import dataclass

POE_ACCESS_KEY = os.getenv("POE_ACCESS_KEY")
FAL_KEY = os.getenv("FAL_KEY")


class VideoMaker(fp.PoeBot):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.fal_client = fal_client.AsyncClient(key=FAL_KEY)
        self.http_client = httpx.AsyncClient()

    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        message = request.query[-1]
        images = [
            attachment
            for attachment in message.attachments
            if attachment.content_type.startswith("image/")
        ]
        if not images or len(images) > 1:
            yield fp.PartialResponse(text="Please provide a single image.")
            return

        [image] = images
        yield fp.PartialResponse(text="Creating video...")
        handle = await self.fal_client.submit(
            "fal-ai/fast-svd-lcm",
            {"image_url": image.url, "fps": 6},
        )

        log_index = 0
        async for progress in handle.iter_events(with_logs=True):
            if isinstance(progress, fal_client.Queued):
                yield fp.PartialResponse(text=f"Queued... {progress.position}")
            elif isinstance(progress, fal_client.InProgress):
                logs = [log["message"] for log in progress.logs[log_index:]]
                log_index = len(progress.logs)
                yield fp.PartialResponse(text="\n".join(logs))

        data = await handle.get()
        video_url = data["video"]["url"]

        await self.post_message_attachment(
            message_id=message.message_id,
            download_url=video_url,
        )
        yield fp.PartialResponse(text=f"Video created!", is_replace_response=True)


    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        return fp.SettingsResponse(
            allow_attachments=True,
            introduction_message="Welcome to the video maker bot. Please provide me an image so i can generate a video from it.",
        )


def main():
    bot = VideoMaker(access_key=POE_ACCESS_KEY)
    fp.run(bot)


if __name__ == "__main__":
    main()
