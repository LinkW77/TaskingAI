from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class AviationStack(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        api_key: str = credentials.credentials.get("AVIATION_STACK_API_KEY")

        api_url = f"https://api.aviationstack.com/v1/flights?access_key={api_key}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
