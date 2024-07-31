import json

from bundle_dependency import *
from aiohttp import ClientSession
from config import CONFIG


class GetFlightsRealtime(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        limit: int = plugin_input.input_params.get("limit", None)
        offset: int = plugin_input.input_params.get("offset", None)
        flight_date: str = plugin_input.input_params.get("flight_date", None)
        dep_iata: str = plugin_input.input_params.get("dep_iata", None)
        arr_iata: str = plugin_input.input_params.get("arr_iata", None)
        airline_iata: str = plugin_input.input_params.get("airline_iata", None)
        flight_iata: str = plugin_input.input_params.get("flight_iata", None)

        aviation_stack_api_key: str = credentials.credentials.get("AVIATION_STACK_API_KEY")

        api_url = f"http://api.aviationstack.com/v1/flights?access_key={aviation_stack_api_key}"

        if limit:
            api_url += f"&limit={limit}"

        if offset:
            api_url += f"&offset={offset}"

        if flight_date:
            api_url += f"&flight_date={flight_date}"

        if dep_iata:
            api_url += f"&dep_iata={dep_iata}"

        if arr_iata:
            api_url += f"&arr_iata={arr_iata}"

        if airline_iata:
            api_url += f"&airline_iata={airline_iata}"

        if flight_iata:
            api_url += f"&flight_iata={flight_iata}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    return PluginOutput(data={"result": json.dumps(data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
