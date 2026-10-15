from bom_tools import list_sheets,preview_sheet,search_item
print(preview_sheet.invoke({"sheet": "HIL vatable", "rows": 5}))
print("-" * 40) 
print(search_item.invoke({"text": "10B21"}))