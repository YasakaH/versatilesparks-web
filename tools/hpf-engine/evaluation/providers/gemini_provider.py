# Gemini answer provider — requires GOOGLE_API_KEY in env

import os
from . import AnswerProvider


class GeminiProvider(AnswerProvider):
    def answer(self, question: str) -> str:
        import google.generativeai as genai
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        resp = model.generate_content(question)
        return resp.text, {"provider": "gemini-2.0-flash"}
