import openpyxl
import json

def extract_from_excel(file):
    sheet_json = []

    wb_obj = openpyxl.load_workbook(file)

    sheet_obj = wb_obj.active

    for columns in tuple(sheet_obj.rows):
        sheet_json.append({
            str(columns[0].value):str(columns[1].value)
        })
    return json.dumps(sheet_json)
