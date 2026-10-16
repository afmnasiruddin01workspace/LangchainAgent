from mcp.server.fastmcp import FastMCP
import bom_tools as bt

mcp = FastMCP("bom")

@mcp.tool()
def list_sheets()->str:
    """ List all sheet names in the excel BOM workbook"""
    return "\n".join(bt.list_sheets.invoke({}))

@mcp.tool()
def preview_sheet(sheet: str, rows: int = 8) -> str:
    """Show the first rows of one sheet."""
    return bt.preview_sheet.invoke({"sheet": sheet, "rows": rows})


@mcp.tool()
def search_item(text: str, sheet: str = "") -> str:
    """Search text in one sheet, or in all sheets when sheet is empty."""
    return bt.search_item.invoke({"text": text, "sheet": sheet})


if __name__ == "__main__":
    mcp.run(transport="stdio")