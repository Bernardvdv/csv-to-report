import csv
import logging
from datetime import datetime

# Random
today_date = datetime.today().strftime("%d-%m-%Y").replace("-", "")

# Setup Logging
log_format = (
    "%(asctime)s::%(levelname)s::%(name)s::" "%(filename)s::%(lineno)d::%(message)s"
)
logging.basicConfig(
    filename="logs_" + today_date + ".log", level="INFO", format=log_format
)


class ReadCSVData:
    """ Read all rows from csv file and pass data back as a list"""

    def read_csv(self, csvfilepath):
        try:
            with open(csvfilepath) as csfFile:
                data = csv.DictReader(csfFile)
                data = list(data)
            logging.info(str(len(data)) + " Rows read from CSV")
            return data
        except Exception as e:
            logging.error(str(e))
