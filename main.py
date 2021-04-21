import sys, logging
from datetime import datetime
import itertools, os, csv

import class_read_csv
csv_import_class = class_read_csv.Read_CSV_Data()

# Random
today_date = datetime.today().strftime("%d-%m-%Y").replace("-", "")

# Setup Logging
log_format = (
    "%(asctime)s::%(levelname)s::%(name)s::" "%(filename)s::%(lineno)d::%(message)s"
)
logging.basicConfig(
    filename="logs_" + today_date + ".log", level="INFO", format=log_format
)


def create_table_of_contents(csv_data):

    table_of_contents = {}
    text_file = open("table_of_contents.txt", "w")
    text_file.write("Table of Contents \n")
    text_file.write("\n")
    for i in csv_data:
        table_of_contents[i["Issue key"]] = i["Summary"]
    for key, value in table_of_contents.items():
        text_file.write(key + "\n")
        text_file.write(value + "\n")
        text_file.write("\n")



if __name__ == "__main__":
    csv_data = csv_import_class.read_csv("gaps.csv")
    table_of_contents = create_table_of_contents(csv_data)