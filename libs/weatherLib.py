#!/usr/bin/env python3.14

import sys
import requests
import time
from typing import Optional

def get_weather(location: Optional[str] = None) -> str:
    """
    Fetch weather information from wttr.in service.

    Args:
        location (str, optional): City name, airport code, or any location.
                                If not provided, uses geolocation.

    Returns:
        str: Formatted weather information

    Raises:
        SystemExit: If there's an error fetching weather data
    """
    # Default format: Show only current weather, temperature, and feels like
    format_param = "?format=%l:+%c+%t+feels+like+%f"

    # Construct the URL
    base_url = "https://wttr.in/"
    location_str = location if location else ""
    url = f"{base_url}{location_str}{format_param}"

    try:
        # Fetch weather data with timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        weather_data = response.text.strip()

        if not weather_data:
            error_exit("Received empty response from weather service.")

        return weather_data

    except requests.exceptions.RequestException as e:
        error_exit(f"Failed to fetch weather data: {str(e)}")

def error_exit(message: str) -> None:
    """
    Print error message and exit with status code 1.

    Args:
        message (str): Error message to display
    """
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)

def main():
    """Main function to handle script execution."""
    # Get location from command line arguments if provided
    location = sys.argv[1] if len(sys.argv) > 1 else None

    # Fetch and display weather information
    weather_data = get_weather(location)

    print("Weather Information")
    print("===================")
    print(weather_data)

if __name__ == "__main__":
    main()
