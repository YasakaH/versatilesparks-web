# GPT answer provider — requires OPENAI_API_KEY in env

import os
from . import AnswerProvider


class GPTProvider(AnswerProvider):
    def answer(self, question: str) -> str:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a browser automation expert. Answer the question concisely and accurately."},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        return resp.choices[0].message.content, {"provider": "gpt-4"}
