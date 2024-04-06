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
        yield fp.MetaResponse(
            text="",
            content_type="text/markdown",
            linkify=True,
            refetch_settings=False,
            suggested_replies=False,
        )

        message = request.query[-1]
        images = [
            attachment
            for attachment in message.attachments
            if attachment.content_type.startswith("image/")
        ]
        if not images:
            prompt = message.content
            response = await self.fal_client.run(
                "fal-ai/fast-sdxl",
                arguments={
                    "prompt": f"a realistic {prompt}, cinematic, ultra hd, high quality, video, cinematic, high quality",
                    "negative_prompt": "illustraiton, cartoon, blurry, text, not cinematic",
                    "image_size": {
                        "height": 576,
                        "width": 1024,
                    },
                    "num_inference_steps": 30,
                },
            )
            image_url = response["images"][0]["url"]
        elif len(images) == 1:
            image_url = images[0].url
        else:
            yield fp.PartialResponse(
                text="Please provide a single image or supply a prompt."
            )
            return

        yield fp.PartialResponse(text="Creating video...")
        handle = await self.fal_client.submit(
            "fal-ai/fast-svd-lcm",
            {"image_url": image_url, "fps": 6},
        )

        header = f"![image]({image_url})"
        async for progress in handle.iter_events(with_logs=True):
            if isinstance(progress, fal_client.Queued):
                yield fp.PartialResponse(
                    text=f"{header}\nQueued... {progress.position}",
                    is_replace_response=True,
                )
            elif isinstance(progress, fal_client.InProgress):
                logs = [log["message"] for log in progress.logs]
                text = f"{header}\n```" + "\n".join(logs)
                yield fp.PartialResponse(text=text, is_replace_response=True)

        data = await handle.get()
        video_url = data["video"]["url"]

        await self.post_message_attachment(
            message_id=request.message_id,
            download_url=video_url,
        )
        yield fp.PartialResponse(text=f"Video created!", is_replace_response=True)

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        return fp.SettingsResponse(
            allow_attachments=True,
            introduction_message=(
                "Welcome to the video maker bot (powered by fal.ai). Please provide me a prompt to "
                "start with or an image so i can generate a video from it."
            ),
        )


bot = VideoMaker()
app = fp.make_app(bot, POE_ACCESS_KEY)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
