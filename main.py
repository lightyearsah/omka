import argparse
import logging
import requests
from abc import ABC, abstractmethod
from typing import Any, Dict


class ApiWorkflow(ABC):
    def run(self):
        try:
            args = self.parse_args()
            self.setup_logging(args.verbose)
            data = self.fetch_data(args.api_key, args.endpoint)
            self.summarize_data(data)
        except Exception as e:
            self.handle_error(e)

    def parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Fetch and summarize API data.")
        parser.add_argument('--api-key', required=True, help="API key for authentication")
        parser.add_argument('--endpoint', required=True, help="API endpoint URL")
        parser.add_argument('--verbose', action='store_true', help="Enable verbose logging")
        return parser.parse_args()

    def setup_logging(self, verbose: bool):
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.debug("Logging configured")

    def fetch_data(self, api_key: str, endpoint: str) -> Dict:
        if not api_key:
            logging.error("API key is required to proceed.")
            raise ValueError("Missing API key")

        headers = {'Authorization': f'Bearer {api_key}'}
        logging.info(f"Fetching data from {endpoint}")
        response = requests.get(endpoint, headers=headers)

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise

        logging.info("Data fetched successfully")
        return response.json()

    def summarize_data(self, data: Dict):
        logging.info("Summarizing data")
        if isinstance(data, list):
            logging.info(f"Received list with {len(data)} items")
        elif isinstance(data, dict):
            logging.info(f"Received dictionary with keys: {list(data.keys())}")
        else:
            logging.warning("Data format unknown")

    def handle_error(self, error: Exception):
        logging.critical(f"An error occurred: {error}")


if __name__ == "__main__":
    workflow = ApiWorkflow()
    workflow.run()
