import json
from typing import Any

import requests
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool


class CurrencyAPIError(Exception):
    """Custom exception for currency API errors."""


def _request_json(url: str, timeout: int = 10) -> dict[str, Any]:
    """Fetch and parse JSON from the currency API."""
    try:
        response = requests.get(url, timeout=timeout, verify=False)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise CurrencyAPIError("currency service unavailable") from exc

    try:
        payload = response.json()
    except (json.JSONDecodeError, ValueError) as exc:
        raise CurrencyAPIError("Invalid response format") from exc

    if not isinstance(payload, dict) or "data" not in payload:
        raise CurrencyAPIError("Invalid response format")

    data = payload["data"]
    if not isinstance(data, dict):
        raise CurrencyAPIError("Invalid response format")

    return data


def check_currency_code(currency_code: str) -> dict[str, Any]:
    """Check whether a currency code is valid and return its details."""
    data = _request_json(f"https://hexarate.paikama.co/api/currencies/{currency_code}")

    try:
        return {
            "currency_code": data["code"],
            "currency_name": data["name"],
        }
    except KeyError as exc:
        raise CurrencyAPIError(f"Invalid response format: {exc}") from exc


def convert_currency(source_currency: str, target_currency: str) -> dict[str, Any]:
    """Convert one currency to another and return the exchange rate details."""
    data = _request_json(
        f"https://hexarate.paikama.co/api/rates/latest/{source_currency}?target={target_currency}"
    )

    try:
        return {
            "source": data["base"],
            "target": data["target"],
            "rate": data["mid"],
        }
    except KeyError as exc:
        raise CurrencyAPIError(f"Invalid response format: {exc}") from exc


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="A helpful assistant for converting currencies.",
    instruction="Answer foreign exchange currency conversions by using the tool convert_currency. Use your tool check_currency_code to answer queries about currency codes.",
    tools=[FunctionTool(convert_currency), FunctionTool(check_currency_code)],
)
