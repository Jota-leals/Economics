from pathlib import Path

#ROOT Directory

root_dir = Path(__file__).resolve().parent.parents[2]

# Data Directories

DATA_DIR = root_dir / "data"
raw_data_dir = DATA_DIR / "raw"
Processed_data_dir = DATA_DIR / "processed"

#Reports

reports_dir = root_dir / "reports"

#Projec Settings

Project_name = "Economics"

Start_date = "2026-07-06"


