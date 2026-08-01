from abc import ABC, abstractmethod
import pandas as pd

class datasource(ABC):
    """Base class for all data providers."""

    @abstractmethod
    def download_data(self, *args, **kwargs) -> pd.DataFrame:
        """Download data and return a DataFrame."""
        pass