import sys, logging
from datetime import datetime

from docx import Document

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

inclusion_list = ["GAPS-97", "GAPS-96", "GAPS-95"]


def create_table_of_contents(csv_data):

    try:
        table_of_contents = {}
        document = Document()
        document.add_heading('Table of Contents', 0)
        text_file = open("table_of_contents.txt", "w")
        text_file.write("Table of Contents \n")
        text_file.write("\n")
        for i in csv_data:
            if i["Issue Type"] != "Epic" and i["Issue key"] in inclusion_list:
                table_of_contents[i["Issue key"]] = i["Summary"]
        for key, value in table_of_contents.items():
            text_file.write(key + "\n")
            text_file.write(value + "\n")
            text_file.write("\n")
            document.add_paragraph(key + " : " + value, style='Intense Quote')
            # document.add_paragraph(value, style='Intense Quote')

        document.save('table_of_contents.docx')
    except Exception as e:
        logging.error(str(e))


def create_document(csv_data):

    try:
        text_file = open("items.txt", "w")
        text_file.write("GAPS Items \n")
        text_file.write("\n")
        row_data = {}
        document = Document()
        document.add_heading('Gaps Items', 0)

        for i in csv_data:
            for k, v in i.items():
                if k in ("Issue key", "Summary", "Issue Type", "Description", "Outward issue link (Blocks)",
                         "Outward issue link (Cloners)", "Outward issue link (Relates)",
                         "Custom field (Story point estimate)", "Parent summary", ):
                    if v != "Epic":
                        row_data[k] = check_string(v)
            create_text_file(row_data, text_file, document)
    except Exception as e:
        logging.error(str(e))


def create_text_file(row_data, text_object, doc_obj):
    try:
        for key, value in row_data.items():
            text_object.write(key + "\n")
            text_object.write(value + "\n")
            text_object.write("\n")
            doc_obj.add_paragraph(key, style='Intense Quote')
            doc_obj.add_paragraph(value, style='Normal')

        doc_obj.save('Gaps_Itesm.docx')
    except Exception as e:
        logging.error(str(e))


def check_string(value):
    if len(value) == 0:
        return "N/a"
    else:
        return value


if __name__ == "__main__":
    csv_data = csv_import_class.read_csv("gaps.csv")
    create_table_of_contents(csv_data)
    create_document(csv_data)