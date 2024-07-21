import argparse
import datetime
import logging
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
    dataframe = pd.DataFrame(ws.get_all_records())


def connect_to_worksheet(workbook_name, worksheet_name, create_new_sheet=False, rows=100, cols=10):
    wb = client.open(workbook_name)
    if create_new_sheet is True:
        ws = wb.add_worksheet(worksheet_name, rows, cols)
    else:
        ws = wb.worksheet(worksheet_name)
    return ws


def main(wb_name, ws_name='Arkusz testowy', sql_file='first_query.sql', create_new_sheet=False):
    columns_names = ('id', 'col1', 'col2')
    load_dotenv()
    df = get_data(sql_file, columns_names)
    worksheet = connect_to_worksheet(wb_name, ws_name, create_new_sheet)
    get_data_from_gsheet(worksheet)
    insert_to_gsheet(worksheet, df)


if __name__ == '__main__':
    logging.log(0, datetime.datetime.now())
    parser = argparse.ArgumentParser()
    parser.add_argument("wb", help="name of workbook")
    parser.add_argument("ws", help="name of worksheet")
    parser.add_argument("sql_f", help="name of sql file")
    parser.add_argument("create_new_sh", help="")
    args = parser.parse_args()
    main(args.wb, args.ws, args.sql_f, args.create_new_sh)
