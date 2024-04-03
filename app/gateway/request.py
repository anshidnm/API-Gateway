import aiohttp
import io

from fastapi.responses import StreamingResponse, JSONResponse, Response
from logging_conf import logger


class APIGateway:
    """
    class for functionalities related to
    API calls along services
    """

    def __init__(
        self,
        url,
        method,
        data={},
        params={}
    ):
        self.__url = url
        self.__data = data
        self.__is_json_data = True
        self.__method = method
        self.__params = params

    async def analyze_response(self, response: aiohttp.ClientResponse):
        """
        Analyse response and convert to
        deliverable format
        """
        if response.content_type == "application/json":
            return JSONResponse(
                await response.json(),
                status_code=response.status
            )
        return StreamingResponse(
            io.BytesIO(await response.read()),
            status_code=response.status,
            media_type=response.content_type
        )

    async def find_method(self, client: aiohttp.ClientSession):
        """
        return appropriate client api calls
        according method
        """
        return getattr(client, self.__method)
    
    async def get_api_data(self):
        """
        Costruct data, url and params for api
        """
        api_data = {"url": self.__url}
        if self.__data:
            key = "json" if self.__is_json_data else "data"
            api_data.update({key: self.__data})
        if self.__params:
            api_data.update({"params": self.__params})
        return api_data

    async def make_request(self):
        """
        Make corresponding api and return
        response object.
        """
        client = aiohttp.ClientSession()
        try:
            call_api = await self.find_method(client)
            payload = await self.get_api_data()
            async with call_api(**payload) as response:
                return await self.analyze_response(response)
        except Exception as e:
            logger.error(f"Somthing went wrong: {str(e)}")
        finally:
            await client.close()