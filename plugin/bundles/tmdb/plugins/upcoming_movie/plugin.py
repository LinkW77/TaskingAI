import json
from typing import Dict
from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class UpcomingMovie(PluginHandler):
    async def execute(
        self, credentials: BundleCredentials, execution_config: Dict, plugin_input: PluginInput
    ) -> PluginOutput:
        language: str = plugin_input.input_params.get("language", "en-US")
        page: int = plugin_input.input_params.get("page", 1)
        region: str = plugin_input.input_params.get("region")

        tmdb_api_key = credentials.credentials["TMDB_API_KEY"]

        base_url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={tmdb_api_key}&language={language}&page={page}"

        if region:
            base_url += f"&region={region.upper()}"

        async with ClientSession() as session:
            async with session.get(url=base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"results": json.dumps(data)})
