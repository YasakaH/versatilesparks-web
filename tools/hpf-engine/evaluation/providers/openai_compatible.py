"""Generic OpenAI-compatible provider with retry support and flexible auth."""

import os, json, urllib.request, time


class OpenAICompatibleProvider:
    def __init__(self, name, api_key_env, model, base_url="https://api.openai.com/v1",
                 use_query_key=False):
        self._name = name
        self.api_key = os.environ.get(api_key_env, "")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.use_query_key = use_query_key

    @property
    def name(self):
        return self._name

    def answer(self, question):
        if not self.api_key:
            return f"[{self._name} not available — set API key]", {"provider": self._name, "error": "no_key"}

        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a browser automation expert. Answer concisely and accurately."},
                {"role": "user", "content": question},
            ],
            "temperature": 0.3,
            "max_tokens": 1024,
        }).encode("utf-8")

        url = self.base_url + "/chat/completions"
        headers = {"Content-Type": "application/json"}
        if not self.use_query_key:
            headers["Authorization"] = "Bearer " + self.api_key
        if self.use_query_key:
            url += "?key=" + self.api_key

        for attempt in range(3):
            try:
                req = urllib.request.Request(url, data=payload, headers=headers)
                resp = urllib.request.urlopen(req, timeout=60)
                data = json.loads(resp.read().decode("utf-8"))
                text = data["choices"][0]["message"]["content"]
                return text, {"provider": self._name, "model": self.model}
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 2:
                    time.sleep(2 ** (attempt + 1))
                    continue
                return f"[{self._name} error: {e.code} {e.reason}]", {"provider": self._name, "error": f"HTTP {e.code}"}
            except Exception as e:
                return f"[{self._name} error: {e}]", {"provider": self._name, "error": str(e)}
