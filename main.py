import os.path

import pandas as pd
from dotenv import load_dotenv

from src.connect_to_db import fetch_data
from src.connect_to_excel import client


def get_data(sql_file_name, col_name):
    sql_path = os.path.join('sql_queries', sql_file_name)
    query = open(sql_path, 'r').read()
    data = fetch_data(query)
    return pd.DataFrame(data, columns=col_name) if data else pd.DataFrame


def insert_to_gsheet(ws, data_frame):
    ws.clear()
    ws.update([data_frame.columns.values.tolist()] + data_frame.values.tolist())


def get_data_from_gsheet(ws):
    dataframe = pd.DataFrame(worksheet.get_all_records())
    print(dataframe)


def connect_to_worksheet(workbook_name, worksheet_name, create_new_sheet=False, rows=100, cols=10):
    wb = client.open(workbook_name)
    if create_new_sheet:
        ws = wb.add_worksheet(worksheet_name, rows, cols)
    else:
        ws = wb.worksheet(worksheet_name)
    return ws


if __name__ == '__main__':
    wb_name = 'Plik testowy'
    ws_name = 'Arkusz testowy'
    sql_file = 'first_query.sql'
    columns_names = ('id', 'col1', 'col2')

    load_dotenv()
    df = get_data(sql_file, columns_names)
    worksheet = connect_to_worksheet(wb_name, ws_name, False)
    get_data_from_gsheet(worksheet)
    insert_to_gsheet(worksheet, df)

