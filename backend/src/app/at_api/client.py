import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import httpx
import config

class ATClient:
    def __init__(self): 
        self.session = httpx.AsyncClient(base_url="https://api.at.govt.nz", headers={"Ocp-Apim-Subscription-Key": config.AT_API_KEY})
    
    async def close(self):
        await self.session.aclose()

    async def _get_realtime_data(self, endpoint: str) -> list:
        response = await self.session.get(endpoint)
        response.raise_for_status()
        data = response.json()
        return data.get("response").get("entity")
    
    async def get_vehicle_locations(self) -> list:
        return await self._get_realtime_data("/realtime/legacy/vehiclelocations")