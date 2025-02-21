import base64
from typing import Optional

from loguru import logger

from src.infrastructure.settings import IMGBB_API_KEY


class ImgBBService:
    def __init__(self, http_client: "HttpClient"):
        self.http_client = http_client
        self.api_key = IMGBB_API_KEY
        self.upload_url = "https://api.imgbb.com/1/upload"

    async def upload_image(self, image_bytes: bytes) -> Optional[str]:
        """
        Upload an image to ImgBB and return the URL.
        """
        try:
            encoded_image = base64.b64encode(image_bytes).decode()
            data = {
                "key": self.api_key,
                "image": encoded_image,
            }
            headers = {}
            response = await self.http_client.post(self.upload_url,  headers=headers, data=data)
            return response["data"]["url"]
        except Exception as e:
            logger.error(f"Error uploading to ImgBB: {e}")
            return None
