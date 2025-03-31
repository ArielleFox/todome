from pathlib import Path
import tempfile, os
from typing import Optional
from .colorLib import *
from .settings import load_location
from .weatherLib import get_weather

class WeatherCache:
    def __init__(self):
        self.username = os.environ.get('USER') or os.environ.get('USERNAME')
        self._cache_file: Optional[tempfile.NamedTemporaryFile] = None
        self._cache_path: Optional[Path] = None

    def new_cache(self) -> None:
        """Create a new weather cache file with current weather data."""
        try:
            location: str = load_location(self.username)
            weather_data = get_weather(location)

            # Create a new temporary file that persists until explicitly deleted
            self._cache_file = tempfile.NamedTemporaryFile(mode='w+',
                                                         delete=False,
                                                         prefix='weather_cache_',
                                                         suffix='.txt')
            self._cache_path = Path(self._cache_file.name)

            # Write weather data to cache file
            self._cache_file.write(weather_data)
            self._cache_file.flush()

        except Exception as e:
            print(f"Error creating weather cache: {e}")

    def load_weather(self) -> str:
        """Load weather data from cache file."""
        try:
            if self._cache_path and self._cache_path.exists():
                return self._cache_path.read_text().strip()
            else:
                self.new_cache()
                return self._cache_path.read_text().strip() if self._cache_path else "Weather data unavailable"
        except Exception as e:
            return f"Error loading weather: {e}"

    def cleanup(self) -> None:
        """Clean up temporary cache file."""
        try:
            if self._cache_file:
                self._cache_file.close()
            if self._cache_path and self._cache_path.exists():
                self._cache_path.unlink()
        except Exception as e:
            print(f"Error cleaning up cache: {e}")

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome_screen(verbose: bool = False) -> str:
    """
    Generate welcome screen message.

    Args:
        verbose (bool): Whether to show verbose output

    Returns:
        str: Formatted welcome message
    """
    weather_cache = WeatherCache()

    try:
        if verbose:
            message = f"🦄 {color_pink_bg('TODOME')} List Manager - Type '{color_yellow_fg('help')}' for commands"
        else:
            weather = weather_cache.load_weather()
            message = f"🦄 {color_pink_bg('TODOME')} List Manager | {color_darkgreen_fg(weather)}"
    finally:
        weather_cache.cleanup()

    return message

if __name__ == '__main__':
    weather_cache = WeatherCache()
    try:
        weather_cache.new_cache()
        print(welcome_screen())
    finally:
        weather_cache.cleanup()

# Created/Modified files during execution:
# Temporary file: /tmp/weather_cache_*.txt (exact name is generated at runtime)
