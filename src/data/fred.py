from .base import datasource
import os
import requests
import pandas as pd

from dotenv import load_dotenv


load_dotenv()

class fred(datasource):
    base_url = "https://api.stlouisfed.org/fred"

    def __init__(self,api_key = None):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        

        if self.api_key is None:
            raise ValueError("No se encontro Fred API KEY")
    def _request_fred(self, endpoint, params):
        request_params ={
            **(params or {}),
            "api_key": self.api_key,
            "file_type": "json"
            }

        url = f"{self.base_url}/{endpoint}"

        response = requests.get(url, params=request_params, timeout=30)

        if response.status_code != 200:
            error_data = response.json()
            error_message = error_data.get("error_message", "Unknown error")

            raise Exception(f"Error en la solicitud a FRED: {error_message}")

        return response.json()
        
    def download_data(self, series_id, observation_start=None, observation_end=None):

        params = {
            "series_id": series_id,
        }

        if observation_start is not None:
            params["observation_start"] = observation_start
        if observation_end is not None:
            params["observation_end"] = observation_end
        data = self._request_fred("series/observations", params = params)

        observations = data.get("observations", [])

        dataframe = pd.DataFrame(observations)

        if dataframe.empty:
            return dataframe

        dataframe = dataframe[["date", "value"]].copy()

        dataframe["date"] = pd.to_datetime(dataframe["date"], errors='coerce')

        dataframe["value"] = pd.to_numeric(dataframe["value"], errors='coerce')

        dataframe["series_id"] = series_id

        return dataframe

    def get_info_fred(self, series_id):

        series_id = series_id.upper().strip()

        params = {
            "series_id": series_id,
        }

        data = self._request_fred("series", params=params)

        series_info = data.get("seriess", [])

        if not series_info:
            raise ValueError(f"No se encontró información para la serie con ID: {series_id}")

        return series_info[0]



