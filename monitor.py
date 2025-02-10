import sys
from setup import get_current_money, get_totals, current_row


try:
    args = sys.argv
    limit = int(args[1])

    if limit > current_row:
        print('Argument out of range.')
    else:
        get_totals(limit)
except:
    get_totals()

get_current_money()

