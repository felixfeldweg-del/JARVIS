import httpx

class Mem0Client:
    def __init__(self, base_url: str):
        self.base_url = base_url.strip("/")
        self.client = httpx.Client(
            base_url=base_url,
            timeout=30
        )

    async def add(self, user_id: str, messages: list):
        response = await self.client.post(
            "/memories",
            json={
                "messages": messages,
                "user_id": user_id,
            },
        )

    async def search(self, user_id: str, query: str):
        response = await self.client.post(
            "/search",
            json={
                "query": query,
                "filters": {
                    "user_id": user_id,
                },
            },
        )

        response.raise_for_status()
        return response.json()

    async def get_all(self, user_id: str):
        r = await self.client.get(
            "/memories",
            params={"user_id": user_id},
        )
        r.raise_for_status()
        return r.json()["results"]

    async def close(self):
        await self.client.aclose()