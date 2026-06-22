from pathlib import Path
import json


def load_config():
    config_parent_path = Path(__file__).resolve().parent

    config_path = config_parent_path/"config.json"

    with open (config_path, "r") as f:
        return json.load(f)