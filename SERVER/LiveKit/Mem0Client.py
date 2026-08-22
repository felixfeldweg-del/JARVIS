import httpx


class Mem0Client:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def add(self, user_id: str, messages: list):
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/memories",
                json={
                    "messages": messages,
                    "user_id": user_id,
                },
            )

            response.raise_for_status()
            return response.json()

    async def search(self, user_id: str, query: str):
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/search",
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
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(
                f"{self.base_url}/memories",
                params={"user_id": user_id},
            )
            r.raise_for_status()
            return r.json()["results"]