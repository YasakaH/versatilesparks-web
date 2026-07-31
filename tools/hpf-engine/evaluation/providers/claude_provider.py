# Claude answer provider — requires ANTHROPIC_API_KEY in env

import os
from . import AnswerProvider


class ClaudeProvider(AnswerProvider):
    def answer(self, question: str) -> str:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        resp = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="You are a browser automation expert. Answer concisely and accurately.",
            messages=[{"role": "user", "content": question}],
        )
        return resp.content[0].text, {"provider": "claude-3-5-sonnet"}
