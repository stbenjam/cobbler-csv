#!/usr/bin/enc python

import csv
import exceptions
from custom_exceptions import *

class CsvParser:
    """
    This is the class that parses your CSV. 
    """

    def __init__(self, csv_file, config):
        self._csv = csv.DictReader(open(csv_file, "rU"), dialect=config.dialect, **{"delimiter": config.delimiter})

    def __iter__(self):
        return self

    def next(self):
        return self._csv.next()
