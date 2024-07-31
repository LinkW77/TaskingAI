import json

from bundle_dependency import *
from datetime import datetime
from aiohttp import ClientSession
from config import CONFIG


def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class GetFlightsHistorical(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        flight_date: str = plugin_input.input_params.get("flight_date")
        limit: int = plugin_input.input_params.get("limit", None)
        offset: int = plugin_input.input_params.get("offset", None)
        dep_iata: str = plugin_input.input_params.get("dep_iata", None)
        arr_iata: str = plugin_input.input_params.get("arr_iata", None)
        airline_iata: str = plugin_input.input_params.get("airline_iata", None)
        flight_iata: str = plugin_input.input_params.get("flight_iata", None)

        aviation_stack_api_key: str = credentials.credentials.get("AVIATION_STACK_API_KEY")

        is_valid = validate_date_format(flight_date)

        if not is_valid:
            raise_http_error("REQUEST_VALIDATION_ERROR", "Flight date must be in YYYY-MM-DD format")

        api_url = (
            f"http://api.aviationstack.com/v1/flights?access_key={aviation_stack_api_key}&flight_date={flight_date}"
        )

        if limit:
            api_url += f"&limit={limit}"

        if offset:
            api_url += f"&offset={offset}"

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
