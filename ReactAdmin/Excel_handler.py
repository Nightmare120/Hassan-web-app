import openpyxl
import json
import string
import random

def extract_from_excel(file):
    sheet_json = []

    wb_obj = openpyxl.load_workbook(file)

    sheet_obj = wb_obj.active

    for columns in tuple(sheet_obj.rows):
        sheet_json.append({
            str(columns[0].value):str(columns[1].value)
        })
    return json.dumps(sheet_json)


def generate_api_project():
    size = 12
    res = "".join(random.choices(string.ascii_letters,k=size))
    return res