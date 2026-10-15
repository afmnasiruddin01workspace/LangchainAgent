from pathlib import Path
import pandas as pd
from langchain_core.tools import tool

BOM_FILE = Path(__file__).parent.parent / "source" / "BOM.xlsx"
ERRORS = r"^#(REF!|DIV/0!|VALUE!|NAME\?|N/A|NUM!|NULL!)$"


def _read(sheet: str) -> pd.DataFrame:
    df = pd.read_excel(BOM_FILE, sheet_name=sheet, header=None, dtype=str)
    return df.replace(ERRORS, pd.NA, regex=True)   # Excel errors become empty


@tool
def list_sheets() -> list[str]:
    """Return the names of all sheets in the BOM workbook."""
    return pd.ExcelFile(BOM_FILE).sheet_names


@tool
def preview_sheet(sheet: str, rows: int = 8) -> str:
    """Show the first rows of one sheet as text, to see what it contains.
    Row numbers are Excel row numbers. Sheet name must match exactly."""
    df = _read(sheet).head(rows)
    lines = []
    for i, row in df.iterrows():
        cells = [str(c) for c in row.dropna()]
        lines.append(f"row {i + 1}: " + " | ".join(cells))
    return "\n".join(lines)


@tool
def search_item(text: str, sheet: str = "") -> str:
    """Search BOM cells for text (case-insensitive), in one sheet or in all
    sheets if no sheet is given. Returns up to 10 matching rows."""
    names = [sheet] if sheet else pd.ExcelFile(BOM_FILE).sheet_names
    hits = []
    for name in names:
        for i, row in _read(name).iterrows():
            cells = [str(c) for c in row.dropna()]
            if any(text.lower() in c.lower() for c in cells):
                hits.append(f"[{name}] row {i + 1}: " + " | ".join(cells))
    return "\n".join(hits[:10]) or "No match."

