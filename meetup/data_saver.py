import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


def save_to_excel(data: list[dict[str, Any]], filename: str = "events_data") -> None:
    """Saves the data to an Excel file in the output directory with a timestamp."""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    full_path = output_dir / f"{filename}_{now}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(full_path, index=False)

    print(f"Data successfully saved to {full_path}.")


def save_to_json(data: list[dict[str, Any]], filename: str = "events_data") -> None:
    """Saves the data to a JSON file in the output directory with a timestamp."""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    full_path = output_dir / f"{filename}_{now}.json"
    with full_path.open("w") as f:
        json.dump(data, f, indent=2)

    print(f"Data successfully saved to {full_path}.")
