from bundle_dependency import *
from typing import Dict
from duckduckgo_search import AsyncDDGS


class SearchText(PluginHandler):
    async def execute(
        self, credentials: BundleCredentials, execution_config: Dict, plugin_input: PluginInput
    ) -> PluginOutput:
        try:
            keywords: str = plugin_input.input_params.get("keywords")
            safe_search = "moderate"

            search_results = await AsyncDDGS().text(keywords=keywords, safesearch=safe_search)
            return PluginOutput(data={"results": search_results})
        except Exception as e:
            raise_provider_api_error(str(e))
