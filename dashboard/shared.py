from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_excel(app_dir / "database.xlsx")
