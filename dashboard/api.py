import json
from pathlib import Path

# Parent directory
app_dir = Path(__file__).parent

with open(app_dir / "ins.json", "r") as file:
  data = json.load(file)

API_KEY = data["API_KEY"]
