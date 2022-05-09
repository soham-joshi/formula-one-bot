from email import parser
import json
import logging
from operator import itemgetter
from tabulate import tabulate
from datetime import date, datetime

from api.config import DATA_DIR
# from f1.errors import MessageTooLongError, DriverNotFoundError

def date_parser(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d %b')


def time_parser(time_str):
    return datetime.strptime(time_str, '%H:%M:%SZ').strftime('%H:%M UTC')

def too_long(message):
    """Returns True if the message exceeds discord's 2000 character limit."""
    return len(message) >= 2000


def make_table(data, headers='keys', fmt='fancy_grid'):
    """Tabulate data into an ASCII table. Return value is a str.

    The `fmt` param defaults to 'fancy_grid' which includes borders for cells. If the table exceeds
    Discord message limit the table is rebuilt with borders removed.

    If still too large raise `MessageTooLongError`.
    """
    table = tabulate(data, headers=headers, tablefmt=fmt)
    # remove cell borders if too long
    if too_long(table):
        table = tabulate(data, headers=headers, tablefmt='simple')
        # cannot send table if too large even without borders
        # Later we need splitting of table into an array of smaller tables to be used by discord
    
    return table


def is_future(year):
    """Return True if `year` is greater than current year."""
    if year == 'current':
        return False
    return datetime.now().year < int(year)
