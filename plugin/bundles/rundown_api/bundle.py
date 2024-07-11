from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class RundownApi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        RUNDOWN_API_API_KEY: str = credentials.credentials.get("RUNDOWN_API_API_KEY")

        api_url = "https://api.apilayer.com/therundown/sports"

        headers = {"apikey": RUNDOWN_API_API_KEY}

        async with ClientSession() as session:
            async with session.get(url=api_url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
