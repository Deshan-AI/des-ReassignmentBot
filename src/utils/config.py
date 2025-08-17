import yaml
import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Credentials:
    URL: str
    USERNAME: str
    PASSWORD: str

class Config:
    """Configuration manager"""
    
    def __init__(self):
        self._config_path = os.path.join(os.path.dirname(__file__), "../../config.yaml")
        self._load_config()

    def _load_config(self):
        """Load and validate configuration"""
        with open(self._config_path, "r") as file:
            config = yaml.safe_load(file)

        # Convert credentials to strongly typed objects
        self.CREDENTIALS = {
            "ERP": Credentials(**{k.upper(): v for k, v in config["ERP"].items()}),
            
        }

       

        self.DATA_PATHS = {
            "BASE": config["data_path"]["Base"],
            
        }

        
        self.MAX_SLEEP = config['sleep']['max']
        self.MIN_SLEEP = config['sleep']['min']
 
