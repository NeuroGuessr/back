from httpx import AsyncClient
import json

class LevelManager:
    def __init__(self):
        print("@authored by god's strongest caffeine consumer")
        self.URL = "http://localhost:8001/"
        self.categories = {}
        self.images = []
        
    async def fetch_all(self):
        await self.fetch_categories()
        
        for key in self.categories.keys():
            response = await self.fetch_images(1, 4, key)
            print("aaaaa", response)
            self.images.append(response)
        
    async def fetch_categories(self):
        url = self.URL + "category"
        response = await AsyncClient().get(url)
        self.categories = json.loads(response.json())
        print(self.categories)
        
    async def fetch_images(self, stages: int, stage_size: int, key: str):
        request_body = {
            'stages': stages,
            'stage_batch_size': stage_size
        }
        url = self.URL + "category/"
        client = AsyncClient()
        body = json.dumps(request_body).encode('utf-8')
        if key == "":
            url += "random"
            response = await client.post(url, content=body)
            return json.loads(response.json())
        else:
            response = await client.post(url + key, content=body)
            return json.loads(response.json())