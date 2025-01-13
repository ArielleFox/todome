#!/usr/bin/env python3.14
import yaml
from pathlib import Path
from typing import Optional

def ensure_config_file() -> Path:
    """Ensure config directory and file exist"""
    config_path = Path.home() / '.config' / 'todome' / 'config.yaml'
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if not config_path.exists():
        with open(config_path, 'w') as f:
            yaml.dump({}, f)
    return config_path

def load_setting(key: str, prompt: str) -> Optional[str]:
    """Generic function to load a setting from config"""
    config_path = ensure_config_file()

    try:
        with open(config_path, 'r') as stream:
            config = yaml.safe_load(stream) or {}
            if key in config:
                return config[key]
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None
    except Exception as e:
        print(f"Error reading config: {e}")
        return None

    # If we get here, we need to set the value
    value = input(prompt).strip()
    try:
        with open(config_path, 'r') as stream:
            config = yaml.safe_load(stream) or {}
        config[key] = value
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        return value
    except Exception as e:
        print(f"Error saving config: {e}")
        return None

def load_location(username: str) -> Optional[str]:
    """Load location setting from config"""
    return load_setting('location', 'Your weather location: ')

def load_time_format(username: str) -> Optional[str]:
    """Load time format setting from config"""
    return load_setting('time_format', '24h format (True) or AM/PM format (False): ')

# Created/Modified files during execution:
# ~/.config/todome/config.yaml
