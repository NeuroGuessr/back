from httpx import AsyncClient
import json

class ImageFetchManager:
    def __init__(self):
        print("@authored by god's strongest caffeine consumer")
        self.URL = "http://localhost:8001/"
        self.categories = {}
        
    async def fetch_categories(self):
        url = self.URL + "category"
        response = await AsyncClient().get(url)
        self.categories = response.json()
    
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
            print(response)
        else:
            response = await client.post(url, params={'key': str(key)}, content=body)
            print(response)