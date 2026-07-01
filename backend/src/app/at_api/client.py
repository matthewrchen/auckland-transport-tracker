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
    
    async def get_combined_feed(self) -> list:
        """ Gets all realtime entities (trip, vehicle, alert)

        Returns:
            [list of trip, vehicle, alert entities]
        """
        return await self._get_realtime_data("/realtime/legacy/")
    
    async def get_trip_updates(self) -> list:
        """ Gets realtime trip update entities

        Returns:
            [list of trip entities]
        """
        return await self._get_realtime_data("/realtime/legacy/tripupdates")

    async def get_vehicle_updates(self) -> list:
        """ Gets realtime vehicle update entities

        Returns:
            [list of vehicle entities]
        """
        return await self._get_realtime_data("/realtime/legacy/vehiclelocations")
    
    async def get_alert_updates(self) -> list:
        """ Gets realtime alert update entities

        Returns:
            [list of alert entities]
        """
        return await self._get_realtime_data("/realtime/legacy/servicealerts")