"""CSV-based database handler for patient data."""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Any
import os


class CSVDatabase:
    """Handle CSV file operations as database."""

    def __init__(self, base_path: str = "./data"):
        """Initialize CSV database."""
        self.base_path = Path(base_path)
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary data directories if they don't exist."""
        directories = [
            "patients",
            "vitals",
            "alerts",
            "research/external_papers",
            "research/internal_research",
            "guidelines",
            "agents",
            "demo"
        ]
        for directory in directories:
            (self.base_path / directory).mkdir(parents=True, exist_ok=True)

    def read_csv(self, file_path: str) -> pd.DataFrame:
        """Read CSV file and return DataFrame."""
        full_path = self.base_path / file_path
        if not full_path.exists():
            return pd.DataFrame()
        try:
            return pd.read_csv(full_path)
        except Exception as e:
            print(f"Error reading CSV {file_path}: {e}")
            return pd.DataFrame()

    def write_csv(self, file_path: str, data: pd.DataFrame, mode: str = 'w'):
        """Write DataFrame to CSV file."""
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if mode == 'a' and full_path.exists():
                data.to_csv(full_path, mode='a', header=False, index=False)
            else:
                data.to_csv(full_path, mode='w', header=True, index=False)
            return True
        except Exception as e:
            print(f"Error writing CSV {file_path}: {e}")
            return False

    def append_row(self, file_path: str, row_data: Dict[str, Any]):
        """Append a single row to CSV file."""
        full_path = self.base_path / file_path
        df = pd.DataFrame([row_data])
        return self.write_csv(file_path, df, mode='a')

    def query(self, file_path: str, filters: Dict[str, Any]) -> pd.DataFrame:
        """Query CSV with filters."""
        df = self.read_csv(file_path)
        if df.empty:
            return df

        for column, value in filters.items():
            if column in df.columns:
                df = df[df[column] == value]

        return df

    def update_row(self, file_path: str, row_id: str, id_column: str, updates: Dict[str, Any]):
        """Update a specific row in CSV."""
        df = self.read_csv(file_path)
        if df.empty:
            return False

        mask = df[id_column] == row_id
        for column, value in updates.items():
            if column in df.columns:
                df.loc[mask, column] = value

        return self.write_csv(file_path, df)

    def delete_row(self, file_path: str, row_id: str, id_column: str):
        """Delete a specific row from CSV."""
        df = self.read_csv(file_path)
        if df.empty:
            return False

        df = df[df[id_column] != row_id]
        return self.write_csv(file_path, df)


# Global database instance
db = CSVDatabase()
