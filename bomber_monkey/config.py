import json
import logging
from pathlib import Path


def setup_logs(config_path: Path):
    with config_path.open() as fp:
        config = json.load(fp)

    logging.basicConfig(**config['log'])
