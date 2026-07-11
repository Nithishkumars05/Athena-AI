from models.base_model import BaseModel

from app.config import client
from app.settings import settings
from services.conversation_service import conversation_service

from pathlib import Path


class GeminiModel(BaseModel):


    def _build_contents(self, prompt, image_path=None):
        """
        Build Gemini multimodal input.
        Supports text + image.
        """

        if image_path and Path(image_path).exists():

            with open(image_path, "rb") as image_file:

                image_bytes = image_file.read()


            return [
                {
                    "text": prompt
                },
                {
                    "inline_data": {
                        "mime_type": self._get_mime_type(image_path),
                        "data": image_bytes
                    }
                }
            ]


        return prompt



    def _get_mime_type(self, image_path):

        extension = Path(image_path).suffix.lower()


        mime_types = {

            ".png": "image/png",

            ".jpg": "image/jpeg",

            ".jpeg": "image/jpeg",

            ".bmp": "image/bmp",

        }


        return mime_types.get(
            extension,
            "image/jpeg"
        )



    def generate(
        self,
        user_name,
        prompt,
        original_message=None,
        image_path=None,
    ):


        conversation_service.save_user_message(
            user_name,
            original_message or prompt
        )


        contents = self._build_contents(
            prompt,
            image_path
        )


        response = client.models.generate_content(

            model=settings.get_model(),

            contents=contents,

            config={
                "temperature": settings.get_temperature()
            }
        )


        if hasattr(response, "text") and response.text:

            answer = response.text.strip()

        else:

            answer = "Sorry, I couldn't generate a response."



        conversation_service.save_ai_message(
            user_name,
            answer
        )


        return answer



    def stream_generate(
        self,
        user_name,
        prompt,
        original_message=None,
        image_path=None,
    ):


        conversation_service.save_user_message(
            user_name,
            original_message or prompt
        )


        contents = self._build_contents(
            prompt,
            image_path
        )


        stream = client.models.generate_content_stream(

            model=settings.get_model(),

            contents=contents,

            config={
                "temperature": settings.get_temperature()
            }
        )


        full_response = ""


        for chunk in stream:

            if hasattr(chunk, "text") and chunk.text:

                full_response += chunk.text

                yield chunk.text



        conversation_service.save_ai_message(
            user_name,
            full_response
        )