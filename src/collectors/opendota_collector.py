import time
import json
import requests


class OpenDotaCollector():

    def __init__(self):
        self.base_url = "https://api.opendota.com/api"
        self.delay = 0.5

    def _get_data(self, endpoint):
        try:
            time.sleep(self.delay)
            response = requests.get(f"{self.base_url}/{endpoint}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Collector error: {e}")
            return None

    def get_matches(self, account_id):
        endpoint = f"players/{account_id}/matches"
        return self._get_data(endpoint)

    def get_matches_info(self, match_id):
        endpoint = f"matches/{match_id}"
        return self._get_data(endpoint)

    def get_heroes(self):
        endpoint = "heroes"
        return self._get_data(endpoint)

    def get_items(self):
        endpoint = "constants/item_ids"
        return self._get_data(endpoint)

    def get_match_details(self, account_id, matches_count=5):
        match_list = self.get_matches(account_id)
        if not match_list:
            print("No matches found")
            return []
        match_details = []
        for match in match_list[:matches_count]:
            details = self.get_matches_info(match['match_id'])
            if details:
                match_details.append(details)
                
        return match_details
