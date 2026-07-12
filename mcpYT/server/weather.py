from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# init fastMCP server
mcp = FastMCP("weather")


# constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"



async def make_nws_request(url: str)->dict[str, Any] | None:
    """make a request to the NWS API with proper error | handling
    """

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None                 

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string
    """        
    props = feature["properties"]

    return f"""
    Event: {props.get("event","Unknown")}
    Area: {props.get("areaDesc","Unknown")}
    Severity: {props.get("severity","Unknown")}
    Description: {props.get("description","No description available.")}
    Instructions: {props.get("instruction","No instructions available.")}
    """


@mcp.tool()
async def get_alerts(state: str)-> str:
    """Get active weather alerts for a given state
    """
    url = f"{NWS_API_BASE}/alerts/active?area={state.upper()}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "No alerts found or failed to fetch data."

    features = data["features"]
    if not features:
        return "No active alerts for this state."

    formatted_alerts = [format_alert(feature) for feature in features]
    return "\n\n".join(formatted_alerts)


@mcp.resource("config://app")
def get_config() -> dict[str, Any]:
    """Get the configuration for the weather app
    """
    return {
        "name": "Weather App",
        "version": "1.0",
        "description": "A simple weather app that fetches alerts from the NWS API."
    }
