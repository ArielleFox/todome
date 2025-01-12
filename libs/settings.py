import yaml
import os
from pathlib import Path
from typing import Optional

def load_location(username: str) -> Optional[str]:
    """
    Load location from user's config file or prompt for it if not set.

    Args:
        username (str): Username to locate config file

    Returns:
        Optional[str]: Location string if successful, None if error occurs
    """
    # Use pathlib for cross-platform path handling
    config_path = Path.home() / '.config' / 'todome' / 'config.yaml'

    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if config_path.exists():
            with open(config_path, 'r') as stream:
                try:
                    config = yaml.safe_load(stream)
                    if config and 'location' in config:
                        return config['location']
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML file: {e}")

        # If we get here, either file doesn't exist or location isn't set
        print("Location not set in config file...")
        location = input('What location are you at?: ').strip()

        # Write new config
        config = {'location': location}
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        return location

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    location = load_location(os.getenv('USER', ''))
    print(f"Location: {location}")

# Created/Modified files during execution:
# ~/.config/todome/config.yaml
