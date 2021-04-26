import class_read_csv
import logging
from datetime import datetime
from htmldocx import HtmlToDocx

from confluence_wiki.bullet import OrderedBulletList, UnOrderedBulletList
from confluence_wiki.text import parse_bold, parse_heading


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

inclusion_list = {"Versioning for Admin View": ["GAPS-17"],
                  "Content Expiry Reporting": ["GAPS-20", "GAPS-83", "GAPS-89", "GAPS-88", "GAPS-93", "GAPS-25",
                                               "GAPS-30", "GAPS-87", "GAPS-24", "GAPS-26", "GAPS-29", "GAPS-23",
                                                "GAPS-27", "GAPS-21", "GAPS-22", "GAPS-28", "GAPS-90", "GAPS-91",
                                                "GAPS-92"],
                  "Compliance Workflows": ["GAPS-36", "GAPS-37", "GAPS-38", "GAPS-39", "GAPS-40"],
                  "UI/UX Improvements to Django interface": ["GAPS-48", "GAPS-49", "GAPS-50", "GAPS-97", "GAPS-51",
                                                            "GAPS-52", "GAPS-53", "GAPS-54", "GAPS-9", "GAPS-47"],
                  "CMS 4.0 Regressions": ["GAPS-56", "GAPS-57",
                  "GAPS-59", "GAPS-60", "GAPS-61", "GAPS-62", "GAPS-63", "GAPS-64", "GAPS-66", "GAPS-67", "GAPS-68",
                  "GAPS-69", "GAPS-70", "GAPS-71", "GAPS-72", "GAPS-73", "GAPS-74", "GAPS-79", "GAPS-80", "GAPS-81"],
                  "Page Admin Enhancements": ["GAPS-31", "GAPS-33", "GAPS-34", "GAPS-45", "GAPS-46"]

                  }


def create_document(csv_data):

    try:
        html_file = open("temp.html", "w")
        html_file.write("<!DOCTYPE html>\n")
        html_file.write("<html>\n")
        html_file.write("<body>\n")
        row_data = {}

        for key, val in inclusion_list.items():
            html_file.write(f"<h1> {key} </h1>\n")
            for a in val:
                for i in csv_data:
                    if i["Issue key"] == a:
                        row_data["Issue key"] = check_string(i["Issue key"])
                        row_data["Summary"] = check_string(i["Summary"])
                        row_data["Description"] = check_string(i["Description"])

                html_file.write(f"<h3> {row_data['Issue key']} : {row_data['Summary']} </h3>\n")
                line = row_data['Description']
                line = OrderedBulletList(line).parse_string()
                line = UnOrderedBulletList(line).parse_string()
                line = replace_image(line)
                line = parse_bold(line)
                line = parse_heading(line)
                html_file.write(f"{line}\n")

        html_file.write("</body>\n")
        html_file.write("</html>\n")

        # Convert HTML file to docx
        new_parser = HtmlToDocx()
        new_parser.parse_html_file("temp.html", "gaps_items_html_converted")

    except Exception as e:
        logging.error(str(e))


def check_string(value):
    if len(value) == 0:
        return "N/a"
    else:
        return value


def replace_image(source):
    if source[0] == "!":
        return "Image Removed"
    else:
        return source


if __name__ == "__main__":
    csv_data = csv_import_class.read_csv("gaps.csv")
    create_document(csv_data)
