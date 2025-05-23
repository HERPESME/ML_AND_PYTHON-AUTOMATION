import os
import yaml


def load_config(config_path="config/config.yaml"):
    """
    Load configuration from YAML and override with environment variables.
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    # Override config values with environment variables
    for key in config:
        env_val = os.getenv(key.upper())
        if env_val is not None:
            try:
                # Attempt to parse numeric or boolean values
                config[key] = yaml.safe_load(env_val)
            except yaml.YAMLError:
                config[key] = env_val

    return config
