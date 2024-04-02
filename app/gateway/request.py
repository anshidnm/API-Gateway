import aiohttp


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
        self.__method = method
        self.__params = params

    def find_method(self, cleint: aiohttp.ClientSession):
        methods = {
            "get": cleint.get,
            "post": cleint.post,
            "put": cleint.put,
            "patch": cleint.patch,
            "delete": cleint.delete
        }
        return methods[self.__method]

    async def make_request(self):
        cleint = aiohttp.ClientSession()
        try:
            call_api = self.find_method(cleint)
            cleint.put()
            response = await call_api()
        except Exception as e:
            print(".....", e)
        finally:
            pass